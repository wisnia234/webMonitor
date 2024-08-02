import os
from datetime import datetime
from websiteResult import WebsiteResult


def generateFile(websiteResults: WebsiteResult) -> str:
    currentDate = getCurrentDate()
    targetDirectoryName = "websiteResult"
    targetFileName = f"{currentDate}websiteMonitorResult.txt"

    targetDirectoryPath = createDirectory(targetDirectoryName)
    targetFilePath = os.path.join(targetDirectoryPath, targetFileName)

    with open(targetFilePath, 'w') as f:
        f.write(f'Connections statuses:')
        for index, result in enumerate(websiteResults, start=1):
            f.write(f'{index}. {result.url}: {result.status}\n')
    
    return targetFilePath


def getCurrentDate() -> str:
    current_datetime = datetime.now()
    return current_datetime.strftime('%Y-%m-%d-%H-%M-%S')

def getCurrentDirectory() -> str:
    return os.path.abspath(os.getcwd())

def createDirectory(targetDirectoryName: str) -> str:
    currentDirectory = getCurrentDirectory()
    targetDirectoryPath = os.path.join(currentDirectory, targetDirectoryName)

    if not os.path.isdir(targetDirectoryPath):
        os.mkdir(targetDirectoryPath)

    return targetDirectoryPath