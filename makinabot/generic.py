#!/usr/bin/python3
import sys, os, subprocess, random, time, requests, re, json, logging
import urllib.request
from datetime import datetime
from keep_alive import keep_alive
from bs4 import BeautifulSoup
import urllib.parse
from telethon import errors
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from telethon import TelegramClient
from telethon.sessions import StringSession
session=str(os.environ['TGSESSION'])
api_id = os.environ['API_ID']
api_hash = os.environ['API_HASH']
chat_id = os.environ['CHAT_ID']
client = TelegramClient(StringSession(session), api_id, api_hash)
keep_alive()

def gethtml(url):
    return BeautifulSoup(requests.get(url).text,'html.parser')

def download_video(id,mode,hash):
    return hash

def getvideo(url):
    temp=url.split('|')
    url=temp[0].strip()
    try:
      name=temp[1].strip()
    except:
      name=None
      
    reid=re.compile('[A-Za-z0-9\-]+')
    id=reid.findall(url)[-1]
    link = requests.post(f'https://www.fembed.com/api/source/{id}').json()['data'][0]['file']
        #link = requests.post(f'https://www.fembed.com/api/source/{id}').json()['data'][1]['file']
       
    if not name:
        name_command = ["youtube-dl",'--referer',f'{link}', f'{link}', "--no-check-certificate", "--get-filename", "-c", "-o", "%(title)s"]
        name=subprocess.check_output(name_command).decode("utf-8")[:-1]
           
    video_file=f'/tmp/{name}.mp4'
    file_command = ["youtube-dl", link, "-i", "-f", "best", "-o", video_file]
        
    return video_file, file_command
    
def showme(sent,total):
    progress=str(round(float(sent*100/total),2))
    decimal=progress.split('.')[-1]
    if len(decimal)==1:
        progress+='0'
    print(f'Sent {sent} bytes of {total} ({progress}%)                 ')

async def main():
    lista=sys.argv[1]
    try:
      with open(sys.argv[1],'r') as file:
            videos=file.read().split('\n')
    except:
        print('File not especified or not found')
        exit()
      
    if videos[-1]=='':
        videos=videos[:-1]

    try:
        with open(f'{lista}.start.txt','r') as begin:
            start=int(begin.read())
    except:
        start=1
        with open(f'{lista}.start.txt','w') as update:
            update.write(str(start))
        

    end=len(videos)
    if start>end:
        print('List finished')
        try:
            os.rename(f'{lista}',f'{lista}.finished.txt')
        except:
            pass
        exit()

    videos=videos[start-1:end]
    if not videos:
      print('List empty')
      exit()

    #await client.send_message(chat_id, 'List start')
    print('List start')
    for i in range(len(videos)):
        print(start)
        url=videos[i]
        if url.startswith('#'):
          try:
            await client.send_message(chat_id, url[1:])
          except errors.FloodWaitError as e:
              print('Have to sleep', e.seconds, 'seconds')
              await client.send_message(chat_id, f'Waiting {e.seconds} seconds')
              time.sleep(e.seconds)
        else:
            try:
                video_file,file_command=getvideo(url)
                subprocess.run(file_command+['--newline'])
                try:
                    metadata = extractMetadata(createParser(video_file))
                    pos=str(random.randrange(0,int(metadata.get('duration').seconds)))
                except:
                    pos='90'

                pic='.'.join(video_file.split('.')[:-1])+'.jpg'
                pic_command = ["ffmpeg", "-ss", pos, "-y", "-i", video_file, "-v:f", "1", pic]
                subprocess.run(pic_command)
                print(f'Sending file {video_file}:')

                while True:
                    try:
                        #await client.send_file(chat_id, video_file,caption='.'.join(video_file.split('/')[-1].split('.')[:-1]),progress_callback=showme,force_document=False,supports_streaming=True,thumb=pic)
                        await client.send_file(chat_id, video_file,caption='.'.join(video_file.split('/')[-1].split('.')[:-1]),progress_callback=showme,force_document=False,supports_streaming=True,thumb=pic)
                        break
                    #await client.send_file('me', video_file,caption='.'.join(video_file.split('/')[-1].split('.')[:-1]),progress_callback=showme,force_document=False,supports_streaming=True,thumb=pic)
                    except errors.FloodWaitError as e:
                        print('Have to sleep', e.seconds, 'seconds')
                        await client.send_message(chat_id, f'Waiting {e.seconds} seconds')
                        time.sleep(e.seconds)
                    except Exception as e:
                        print(f'Error {str(e)}')
                        await client.send_message(chat_id, f'Error found: {str(e)}')
                        break
            except Exception as e:
                print(f'Error {str(e)}')
                await client.send_message(chat_id, f'Error found: {str(e)}')
                continue
        try:
            os.remove(video_file)
            os.remove(pic)
        except:
            pass



        start+=1
        with open(f'{lista}.start.txt','w') as update:
            update.write(str(start))

with client:
    client.loop.run_until_complete(main())
  
