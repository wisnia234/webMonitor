import asyncio
import aiohttp
import fileResponseGenerator
import mailSender
from typing import List
from websiteResult import WebsiteResult
import googleStorageClient
import ntpath

urls = [
    "https://localhost:7247/200response",
    "https://localhost:7247/400simulation",
    "https://localhost:7247/500simulation",
    "https://localhost:7247/noServerResponseSimulation",
    ]

def run() -> None:
    websiteResults = asyncio.run(runWebsiteRequest())
    filePath = generateResultFile(websiteResults)
    sendFileToCloudStorage(filePath)
    handleWebsiteResults(websiteResults)
    displayResults(websiteResults)

async def runWebsiteRequest() -> List[WebsiteResult]:
    timeout = aiohttp.ClientTimeout(total=4)
    async with aiohttp.ClientSession(timeout=timeout) as clientSession:
        websiteResult = await getAllWebsiteResults(clientSession, urls)
        await clientSession.close()
        return websiteResult

async def fetch(clientSession: aiohttp.ClientSession, url: str) -> WebsiteResult:
    try:
        async with clientSession.get(f'{url}') as response:
            return WebsiteResult(url, response.status)
    except:
        status = "The connection could not be established."
        return WebsiteResult(url, status)

async def getAllWebsiteResults(clientSession: aiohttp.ClientSession, urls: List[str]) -> List[WebsiteResult]:
    tasks = []
    for url in urls:
        task = asyncio.create_task(fetch(clientSession, url))
        tasks.append(task)
    return await asyncio.gather(*tasks)
        
def displayResults(websiteResults: WebsiteResult) -> None:
    for index, result in enumerate(websiteResults, start=1):
            print(f'{index}. {result.url}: {result.status}')
    print('\n')

def createErrorMessage(unsuccessfulWebsiteResults: WebsiteResult) -> str:
    results = []
    for index, result in enumerate(unsuccessfulWebsiteResults, start=1):
        results.append(f'{index}. {result.url}: {result.status}\n')
    result_string = ''.join(results)

    return result_string

def sendErrorMessage(errorMessage: str) -> None:
    mailSender.sendErrorMessage(errorMessage)

def getUnsuccessfulWebsiteResults(websiteResults: List[WebsiteResult]) -> List[WebsiteResult]:
    return [result for result in websiteResults if (type(result.status) is int and result.status >= 400) or type(result.status) is str ]

def generateResultFile(websiteResults: List[WebsiteResult]) -> str:
    return fileResponseGenerator.generateFile(websiteResults)

def sendFileToCloudStorage(filePath: str) -> None:
    blobName = ntpath.basename(filePath).split('.')[0]
    googleStorageClient.upload_to_bucket(blobName, filePath)

def handleWebsiteResults(websiteResults: List[WebsiteResult]) -> None:
    errorWebsiteResults = getUnsuccessfulWebsiteResults(websiteResults)
    if len(errorWebsiteResults) != 0:
        errorMessage = createErrorMessage(errorWebsiteResults)
        sendErrorMessage(errorMessage)