from config import settings
from models import ProfileCreate, ProfileUpdate
from service import Service
import httpx

class ProfileService(Service):
    def __init__(self):
        self._build_base_url(
            host = settings.prof_url.host,
            port = settings.prof_url.port 
        )

    
    async def create_profile(
        self,
        username: str,
        first_name: str,
        last_name: str,
        email: str,
        phone: str
    ):
        url = self._build_endpoint_url(settings.prof_url.register_endpoint)

        new_profile = ProfileCreate(
            username = username,
            firstName = first_name,
            lastName = last_name,
            email = email,
            phone = phone
        )

        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json = new_profile.model_dump()
            )

        self._check_response(response)

        return response


    async def delete_profile(
        self,
        username: str
    ):
        url = self._build_endpoint_url(settings.prof_url.del_endpoint, username)

        async with httpx.AsyncClient() as client:
            response = await client.delete(url)

        self._check_response(response)

        return response
    

    async def get_profile(
        self,
        username: str
    ):
        url = self._build_endpoint_url(settings.prof_url.get_endpoint, username)

        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        self._check_response(response)

        return response

        
    async def upd_profile(
        self,
        username: str,
        profile_upd: ProfileUpdate
    ):
        url = self._build_endpoint_url(settings.prof_url.upd_endpoint, username)

        async with httpx.AsyncClient() as client:
            response = await client.put(
                url,
                json = profile_upd.model_dump()
            )

        self._check_response(response)

        return response 



    
