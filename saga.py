from models import UserCreate, ProfileReturn
from service_auth import AuthService
from service_profile import ProfileService
from service_billing import BillingService


class SagaRegister():

    def __init__(self):
        self.__auth_created    = False
        self.__profile_created = False
        self.__wallet_created  = False

    async def execute_saga(
        self,
        reg_data: UserCreate
    ):
        auth_service    = AuthService()
        profile_service = ProfileService()
        billing_service = BillingService()

        try:            
            auth_response = await auth_service.create_auth(reg_data.username, reg_data.password)
            self.__auth_created = True

            profile_response = await profile_service.create_profile(reg_data.username,
                                                                    reg_data.firstName,
                                                                    reg_data.lastName,
                                                                    reg_data.email,
                                                                    reg_data.phone)
            self.__profile_created = True

            billing_response = await billing_service.create_wallet(reg_data.username)
            self.__wallet_created = True

        except Exception as e:
            print('Ошибка при регистрации: ' + str(e))
            await self.rollback_saga(reg_data)
            raise

        json = profile_response.json()
        return ProfileReturn(
            username  = json.get("username"),
            email     = json.get("email"),
            phone     = json.get("phone"),
            firstName = json.get("firstName"),
            lastName  = json.get("lastName")
        )


    async def rollback_saga(
        self,
        reg_data: UserCreate
    ):
        auth_service    = AuthService()
        profile_service = ProfileService()
        billing_service = BillingService()

        try:
            if self.__wallet_created:
                billing_response = billing_service.delete_wallet(reg_data.username)
                self.__wallet_created = False
            if self.__profile_created:
                profile_response = await profile_service.delete_profile(reg_data.username)
                self.__profile_created = False
            if self.__auth_created:
                auth_response = await auth_service.delete_auth(reg_data.username)
                self.__auth_created = False
        except Exception as e:
            print('Ошибка при откате регистрации: ' + str(e))
            raise


