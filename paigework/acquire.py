"""
A module for obtaining repo readme and language data from the github API.
Before using this module, read through it, and follow the instructions marked
TODO.
After doing so, run it like this:
    python acquire.py
To create the `data.json` file that contains the data.
"""
import os
import json
from typing import Dict, List, Optional, Union, cast
import requests

from env import github_token, github_username


REPOS = ['SciTools/iris',
 'team-ocean/veros',
 'matplotlib/cmocean',
 'VIAME/VIAME',
 'dankelley/oce',
 'euroargodev/argopy',
 'Alexander-Barth/NCDatasets.jl',
 'chadagreene/CDT',
 'rabernat/intro_to_physical_oceanography',
 'jonathanlilly/jLab',
 'wafo-project/pywafo',
 'hainegroup/oceanspy',
 'nasa/podaacpy',
 'miniufo/xgrads',
 'pyoceans/sea-py',
 'gher-ulg/DIVAnd.jl',
 'MITgcm/xmitgcm',
 'kthyng/python4geosciences',
 'ocefpaf/python4oceanographers',
 'lnferris/ocean_data_tools',
 'clstoulouse/motu-client-python',
 'introocean/introocean-en',
 'aodn/imos-toolbox',
 'nasa/podaac_tools_and_services',
 'DFO-Ocean-Navigator/Ocean-Data-Map-Project',
 'amnh/HackTheDeep',
 'castelao/CoTeDe',
 'stoqs/stoqs',
 'JuliaOcean/AIBECS.jl',
 'gher-ulg/DIVA',
 'lkilcher/dolfyn',
 'OceanLabPy/OceanLab',
 'MikkoVihtakari/ggOceanMaps',
 'powellb/seapy',
 'gher-ulg/DINCAE',
 'OceanMixingCommunity/Standard-Mixing-Routines',
 'gher-ulg/PhysOcean.jl',
 'oscarbranson/cbsyst',
 'gher-ulg/DivaPythonTools',
 'IHCantabria/THREDDSExplorer',
 'SciTools/python-stratify',
 'ocean-data-challenges/2020a_SSH_mapping_NATL60',
 'clstoulouse/motu',
 'iuryt/Panthalassan',
 'VACUMM/vacumm',
 'jerabaul29/OpenMetBuoy-v2021a',
 'gauteh/sfy',
 'JuliaOcean/JuliaOceanSciencesMeeting2020',
 'TEOS-10/GibbsSeaWater.jl',
 'aist-oceanworks/mudrod',
 'obidam/pcm',
 'FinalTheory/oceanography-numerical-calculations',
 'TEOS-10/GSW-Matlab',
 'pyoceans/pocean-core',
 'boshek/rsoi',
 'mjharriso/MIDAS',
 'AtlanticR/bioRworkshops',
 'PlanktoScope/PlanktoScope',
 'Hunter-Github/GitScience',
 'ArgoCanada/argoFloats',
 'omuse-geoscience/omuse',
 'DocOtak/gsw-xarray',
 'njwilson23/narwhal',
 'sea-mat/sea-mat',
 'Energy-Pathways-Group/GLOceanKit',
 'c-proof/pyglider',
 'MPOcanes/MPO624-2018',
 'thunderhoser/ai2es_xai_course',
 'rowg/hfrprogs',
 'jonathansharp/CO2-System-Extd',
 'iuryt/ocean_gyre_tank',
 'janosh/ocean-artup-gatsby',
 'gher-ulg/Diva-Workshops',
 'hackforthesea/awesome-marine-hacking',
 'TEOS-10/GSW-Fortran',
 'ngs-docs/2016-metagenomics-sio',
 'gvoulgaris0/WavePart',
 'gcosne/OceanographyProject',
 'wavebitscientific/ndbc',
 'SHYFEM-model/shyfem',
 'GenSci/NDBC',
 'seaflow-uw/popcycle',
 'FESOM/pyfesom',
 'gher-ulg/Documentation',
 'janadr/time_series_analysis',
 'mvdh7/pytzer',
 'mpiannucci/gribberish',
 'miniufo/xinvert',
 'ctroupin/Python-Course-Cadiz',
 'jinbow/popy',
 'TEOS-10/GSW-R',
 'castelao/GSW-rs',
 'euroargodev/argodmqc_owc',
 'OSU-CEOAS-Schmittner/UVic2.9',
 'pymoc/pymoc',
 'chouj/POPapers',
 'tagbase/tagbase-server',
 'jaanga/terrain-srtm30-plus',
 'CNES/aviso-lagrangian',
 'hackforthesea/2020',
 'SciTools/iris',
 'team-ocean/veros',
 'matplotlib/cmocean',
 'VIAME/VIAME',
 'dankelley/oce',
 'euroargodev/argopy',
 'Alexander-Barth/NCDatasets.jl',
 'chadagreene/CDT',
 'rabernat/intro_to_physical_oceanography',
 'jonathanlilly/jLab',
 'wafo-project/pywafo',
 'hainegroup/oceanspy',
 'nasa/podaacpy',
 'miniufo/xgrads',
 'pyoceans/sea-py',
 'gher-ulg/DIVAnd.jl',
 'MITgcm/xmitgcm',
 'kthyng/python4geosciences',
 'ocefpaf/python4oceanographers',
 'lnferris/ocean_data_tools',
 'clstoulouse/motu-client-python',
 'introocean/introocean-en',
 'aodn/imos-toolbox',
 'nasa/podaac_tools_and_services',
 'DFO-Ocean-Navigator/Ocean-Data-Map-Project',
 'amnh/HackTheDeep',
 'castelao/CoTeDe',
 'stoqs/stoqs',
 'JuliaOcean/AIBECS.jl',
 'gher-ulg/DIVA',
 'lkilcher/dolfyn',
 'OceanLabPy/OceanLab',
 'MikkoVihtakari/ggOceanMaps',
 'powellb/seapy',
 'gher-ulg/DINCAE',
 'OceanMixingCommunity/Standard-Mixing-Routines',
 'gher-ulg/PhysOcean.jl',
 'oscarbranson/cbsyst',
 'gher-ulg/DivaPythonTools',
 'IHCantabria/THREDDSExplorer',
 'SciTools/python-stratify',
 'ocean-data-challenges/2020a_SSH_mapping_NATL60',
 'clstoulouse/motu',
 'iuryt/Panthalassan',
 'VACUMM/vacumm',
 'jerabaul29/OpenMetBuoy-v2021a',
 'gauteh/sfy',
 'JuliaOcean/JuliaOceanSciencesMeeting2020',
 'TEOS-10/GibbsSeaWater.jl',
 'aist-oceanworks/mudrod',
 'obidam/pcm',
 'FinalTheory/oceanography-numerical-calculations',
 'TEOS-10/GSW-Matlab',
 'pyoceans/pocean-core',
 'boshek/rsoi',
 'mjharriso/MIDAS',
 'AtlanticR/bioRworkshops',
 'PlanktoScope/PlanktoScope',
 'Hunter-Github/GitScience',
 'ArgoCanada/argoFloats',
 'omuse-geoscience/omuse',
 'DocOtak/gsw-xarray',
 'njwilson23/narwhal',
 'sea-mat/sea-mat',
 'Energy-Pathways-Group/GLOceanKit',
 'c-proof/pyglider',
 'MPOcanes/MPO624-2018',
 'thunderhoser/ai2es_xai_course',
 'rowg/hfrprogs',
 'jonathansharp/CO2-System-Extd',
 'iuryt/ocean_gyre_tank',
 'janosh/ocean-artup-gatsby',
 'gher-ulg/Diva-Workshops',
 'hackforthesea/awesome-marine-hacking',
 'TEOS-10/GSW-Fortran',
 'ngs-docs/2016-metagenomics-sio',
 'gvoulgaris0/WavePart',
 'gcosne/OceanographyProject',
 'wavebitscientific/ndbc',
 'SHYFEM-model/shyfem',
 'GenSci/NDBC',
 'seaflow-uw/popcycle',
 'FESOM/pyfesom',
 'gher-ulg/Documentation',
 'janadr/time_series_analysis',
 'mvdh7/pytzer',
 'mpiannucci/gribberish',
 'miniufo/xinvert',
 'ctroupin/Python-Course-Cadiz',
 'jinbow/popy',
 'TEOS-10/GSW-R',
 'castelao/GSW-rs',
 'euroargodev/argodmqc_owc',
 'OSU-CEOAS-Schmittner/UVic2.9',
 'pymoc/pymoc',
 'chouj/POPapers',
 'tagbase/tagbase-server',
 'jaanga/terrain-srtm30-plus',
 'CNES/aviso-lagrangian',
 'hackforthesea/2020']
 

headers = {"Authorization": f"token {github_token}", "User-Agent": github_username}

if headers["Authorization"] == "token " or headers["User-Agent"] == "":
    raise Exception(
        "You need to follow the instructions marked TODO in this script before trying to use it"
    )


def github_api_request(url: str) -> Union[List, Dict]:
    response = requests.get(url, headers=headers)
    response_data = response.json()
    if response.status_code != 200:
        raise Exception(
            f"Error response from github api! status code: {response.status_code}, "
            f"response: {json.dumps(response_data)}"
        )
    return response_data


def get_repo_language(repo: str) -> str:
    url = f"https://api.github.com/repos/{repo}"
    repo_info = github_api_request(url)
    if type(repo_info) is dict:
        repo_info = cast(Dict, repo_info)
        return repo_info.get("language", None)
    raise Exception(
        f"Expecting a dictionary response from {url}, instead got {json.dumps(repo_info)}"
    )


def get_repo_contents(repo: str) -> List[Dict[str, str]]:
    url = f"https://api.github.com/repos/{repo}/contents/"
    contents = github_api_request(url)
    if type(contents) is list:
        contents = cast(List, contents)
        return contents
    raise Exception(
        f"Expecting a list response from {url}, instead got {json.dumps(contents)}"
    )


def get_readme_download_url(files: List[Dict[str, str]]) -> str:
    """
    Takes in a response from the github api that lists the files in a repo and
    returns the url that can be used to download the repo's README file.
    """
    for file in files:
        if file["name"].lower().startswith("readme"):
            return file["download_url"]
    return ""


def process_repo(repo: str) -> Dict[str, str]:
    """
    Takes a repo name like "gocodeup/codeup-setup-script" and returns a
    dictionary with the language of the repo and the readme contents.
    """
    contents = get_repo_contents(repo)
    readme_contents = requests.get(get_readme_download_url(contents)).text
    return {
        "repo": repo,
        "language": get_repo_language(repo),
        "readme_contents": readme_contents,
    }


def scrape_github_data() -> List[Dict[str, str]]:
    """
    Loop through all of the repos and process them. Returns the processed data.
    """
    return [process_repo(repo) for repo in REPOS]


if __name__ == "__main__":
    data = scrape_github_data()
    json.dump(data, open("data2.json", "w"), indent=1)