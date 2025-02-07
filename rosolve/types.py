from typing import TypedDict, List, Union, Optional

class ChallengeInfo(TypedDict):
    publicKey: str
    site: str
    surl: str
    capiMode: str
    styleTheme: str
    languageEnabled: bool
    jsfEnabled: bool
    extraData: dict
    ancestorOrigins: List[str]
    treeIndex: List[int]
    treeStructure: str
    locationHref: str

class BrowserInfo(TypedDict):
    Cookie: str
    'Sec-Ch-Ua': str
    'User-Agent': str 