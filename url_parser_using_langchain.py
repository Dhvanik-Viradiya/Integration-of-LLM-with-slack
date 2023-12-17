from langchain.document_loaders import AsyncHtmlLoader
from langchain.document_loaders import PlaywrightURLLoader
import pprint
from langchain.document_transformers import Html2TextTransformer



from youtube_transcript_api import YouTubeTranscriptApi
import pytube
url = "https://youtube.com/watch?v=jFDrv6G5WiU&amp;ab_channel=KRAFTONINDIAESPORTS|hi radhe radhe"
try:
    yt = pytube.YouTube(url)
    transcript_list = YouTubeTranscriptApi.list_transcripts(yt.video_id)
    for transcript in transcript_list:
        transcript = transcript.translate('en').fetch()
        str_transcript = ""
        for data in transcript:
            str_transcript+=" "+data["text"]
        print(str_transcript)
        break
except Exception as e:
    print("Error", e)


urls = ["https://blog.hubspot.com/marketing/how-to-use-medium"]
# # urls = ["https://github.com/Dhvanik-Viradiya/Integration-of-LLM-with-slack"]
# # loader = AsyncHtmlLoader(urls)
# print(dir(PlaywrightURLLoader))
# print(dir(PlaywrightURLLoader.__getattribute__))
# loader = PlaywrightURLLoader(urls=urls, remove_selectors=["header", "footer"])
# docs = loader.load()

# # html2text = Html2TextTransformer()
# # docs_transformed = html2text.transform_documents(docs)
# # print(dir(docs[0]))
# # json_data = docs[0].to_json()
# # title = json_data["kwargs"]["metadata"]["title"] 
# # description = json_data["kwargs"]["metadata"]["description"] 


# # import cleantext
# # import xml.etree.ElementTree
# # data = json_data["kwargs"]["page_content"]
# # # cleaned_text = ''.join(xml.etree.ElementTree.fromstring(data).itertext())
# # from bs4 import BeautifulSoup
# # cleaned_text = BeautifulSoup(data, "lxml").text
# # cleaned_text = cleantext.clean(cleaned_text)
# # open("a.txt", "w").write(data)
# # open("b.txt", "w").write(cleaned_text)
# # print(json_data["kwargs"].keys())
# # for i in json_data:
# #     print(i, json_data[i])
# # print(dir(docs_transformed[0]))
# # pprint.pprint(docs_transformed[0].page_content[1:100])
# # pprint.pprint(docs[0].page_content[1:100])
# # print("".join(docs_transformed[0].page_content))
# # print(docs[0].page_content)