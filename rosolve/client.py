from typing import Optional
from curl_cffi import requests
import asyncio
import aiohttp
from .errors import RoSolveException, InvalidKey, TaskError
from .types import ChallengeInfo, BrowserInfo

class Client:
    """
    Main client for interacting with the RoSolve API
    
    Parameters
    ----------
    api_key: str
        Your RoSolve API key
    session: Optional[aiohttp.ClientSession]
        An optional aiohttp session to use for requests
    """
    
    BASE_URL = "https://rosolve.pro"
    
    def __init__(self, api_key: str, session: Optional[aiohttp.ClientSession] = None):
        self.api_key = api_key
        self._session = session or aiohttp.ClientSession()
        
    async def __aenter__(self):
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
        
    async def close(self):
        """Close the client session"""
        if self._session and not self._session.closed:
            await self._session.close()
            
    async def get_balance(self) -> float:
        """
        Get current balance for the API key
        
        Returns
        -------
        float
            Current balance
        
        Raises
        ------
        InvalidKey
            If the API key is invalid
        """
        async with self._session.get(
            f"{self.BASE_URL}/getBalance",
            params={"key": self.api_key}
        ) as resp:
            data = await resp.json()
            
            if "error" in data:
                raise InvalidKey(data["error"])
                
            return data["balance"]
            
    async def solve_funcaptcha(
        self,
        roblox_session: requests.Session,
        blob: str,
        proxy: str,
        cookie: str,
        max_retries: int = 60,
        retry_delay: float = 1.0
    ) -> Optional[str]:
        """
        Solve a FunCaptcha challenge
        
        Parameters
        ----------
        roblox_session: requests.Session
            The Roblox session object
        blob: str
            The blob data for the challenge
        proxy: str
            Proxy to use for solving
        cookie: str
            Roblox cookie
        max_retries: int
            Maximum number of retries for checking solution
        retry_delay: float
            Delay between retries in seconds
            
        Returns
        -------
        Optional[str]
            The solution token if successful, None if failed
            
        Raises
        ------
        TaskError
            If the task creation fails
        """
        challenge_info: ChallengeInfo = {
            "publicKey": "476068BF-9607-4799-B53D-966BE98E2B81",
            "site": "https://www.roblox.com/",
            "surl": "https://arkoselabs.roblox.com",
            "capiMode": "inline",
            "styleTheme": "default",
            "languageEnabled": False,
            "jsfEnabled": False,
            "extraData": {"blob": blob},
            "ancestorOrigins": ["https://www.roblox.com", "https://www.roblox.com"],
            "treeIndex": [1, 0],
            "treeStructure": "[[],[[]]]",
            "locationHref": "https://www.roblox.com/arkose/iframe"
        }
        
        browser_info: BrowserInfo = {
            'Cookie': cookie,
            'Sec-Ch-Ua': roblox_session.headers["sec-ch-ua"],
            'User-Agent': roblox_session.headers["user-agent"]
        }
        
        payload = {
            "key": self.api_key,
            "challengeInfo": challenge_info,
            "browserInfo": browser_info,
            "proxy": proxy
        }
        
        async with self._session.post(
            f"{self.BASE_URL}/createTask",
            json=payload
        ) as resp:
            data = await resp.json()
            
            if "error" in data:
                raise TaskError(data["error"])
                
            task_id = data["taskId"]
            
        for _ in range(max_retries):
            await asyncio.sleep(retry_delay)
            
            async with self._session.get(
                f"{self.BASE_URL}/taskResult/{task_id}"
            ) as resp:
                solution = await resp.json()
                
                if solution["status"] == "completed":
                    return solution["result"]["solution"]
                elif solution["status"] == "failed":
                    return None
                    
        return None 