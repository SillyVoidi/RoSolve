# RoSolve

An async Python client for the RoSolve API, supporting FunCaptcha solving for Roblox.

## Features

- ✨ Async-first design
- 📝 Type hints for better IDE support
- 🎮 Clean.
- 💻 Cross-platform support (Windows, macOS, Linux)
- 🔄 Automatic retries and error handling
- 🚀 Easy to use with proper session management

## Installation

```bash
pip install rosolve
```

## Quick Start

```python
import asyncio
from rosolve import Client

async def main():
    # Initialize with a default proxy (optional)
    async with Client(
        "your_api_key",
        proxy="http://user:pass@host:port"  # Optional default proxy
    ) as client:
        # Get balance
        balance = await client.get_balance()
        print(f"Current balance: {balance}")

if __name__ == "__main__":
    asyncio.run(main())
```

## FunCaptcha Solving Example

Here's a complete example of solving a FunCaptcha challenge:

```python
import asyncio
from curl_cffi import requests
from rosolve import Client

async def main():
    # Initialize your Roblox session
    roblox_session = requests.Session()
    roblox_session.headers.update({
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0",
        "sec-ch-ua": '"Chromium";v="122", "Google Chrome";v="122"'
    })

    # Your configuration
    api_key = "your_api_key_here"
    cookie = ".ROBLOSECURITY=your_cookie_here"
    
    # Proxy configuration (multiple options)
    default_proxy = "http://user:pass@host:port"  # For all requests
    solving_proxy = "http://other:pass@host:port"  # Just for solving

    async with Client(api_key, proxy=default_proxy) as client:
        try:
            # Solve the FunCaptcha using a specific proxy for this solve
            solution = await client.solve_funcaptcha(
                roblox_session=roblox_session,
                blob="your_blob_data_here",
                proxy=solving_proxy,  # Override default proxy (optional)
                cookie=cookie
            )

            if solution:
                print("Successfully solved captcha!")
                print(f"Token: {solution}")
            else:
                print("Failed to solve captcha")

        except Exception as e:
            print(f"An error occurred: {e}")  # Now with color-coded errors!

if __name__ == "__main__":
    asyncio.run(main())
```

## API Reference

### Client

The main class for interacting with the RoSolve API.

```python
client = Client(
    api_key: str,
    session: Optional[aiohttp.ClientSession] = None,
    proxy: Optional[str] = None  # Default proxy for all requests
)
```

#### Parameters:
- `api_key` (str): Your RoSolve API key
- `session` (Optional[aiohttp.ClientSession]): An optional aiohttp session to use
- `proxy` (Optional[str]): Default proxy to use for all requests

### Methods

#### get_balance()
Get your current RoSolve balance.

```python
balance = await client.get_balance()
```

Returns:
- `float`: Your current balance

Raises:
- `InvalidKey`: If the API key is invalid

#### solve_funcaptcha()
Solve a FunCaptcha challenge.

```python
solution = await client.solve_funcaptcha(
    roblox_session: requests.Session,
    blob: str,
    proxy: str,
    cookie: str,
    max_retries: int = 60,
    retry_delay: float = 1.0
)
```

Parameters:
- `roblox_session` (requests.Session): The Roblox session object
- `blob` (str): The blob data from the challenge
- `proxy` (str): Proxy to use (format: "protocol://user:pass@host:port")
- `cookie` (str): Roblox cookie
- `max_retries` (int, optional): Maximum retries for checking solution. Defaults to 60
- `retry_delay` (float, optional): Delay between retries in seconds. Defaults to 1.0

Returns:
- `Optional[str]`: The solution token if successful, None if failed

Raises:
- `TaskError`: If the task creation fails

### Error Handling

The package provides several custom exceptions with color-coded error messages:

```python
from rosolve import RoSolveException, InvalidKey, TaskError, ProxyError

try:
    solution = await client.solve_funcaptcha(...)
except InvalidKey as e:
    print(e)  # Yellow error message
except TaskError as e:
    print(e)  # Red error message
except ProxyError as e:
    print(e)  # Yellow error message
except RoSolveException as e:
    print(e)  # Red error message
```

## Best Practices

1. Always use the client as a context manager:
```python
async with Client(api_key) as client:
    # Your code here
```

2. Check your balance before heavy usage:
```python
balance = await client.get_balance()
if balance < 10:
    print("Low balance warning!")
```

3. Handle exceptions appropriately:
```python
try:
    solution = await client.solve_funcaptcha(...)
except Exception as e:
    print(f"Error: {e}")
```

4. Use proper proxy formatting:
```python
# With authentication
proxy = "http://username:password@host:port"
proxy = "https://username:password@host:port"
proxy = "socks5://username:password@host:port"

# Without authentication
proxy = "http://host:port"
```

5. Handle proxy configuration flexibly:
```python
# Set default proxy for all requests
client = Client(api_key, proxy="http://user:pass@host:port")

# Override proxy for specific solves
solution = await client.solve_funcaptcha(..., proxy="http://other:pass@host:port")
```

## License

This project is licensed under the Unlicense - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions, please open an issue on GitHub.