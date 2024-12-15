# import webuiapi


# api = webuiapi.WebUIApi()
# api = webuiapi.WebUIApi(host='127.0.0.1', port=7860)


# api = webuiapi.WebUIApi(sampler='Euler a', steps=3)

# result = api.txt2img(prompt="cute squirrel",
#                     seed=0,
#                     cfg_scale=1,
#                     sampler_index='Simple',
#                     steps=3,
#                     enable_hr=False,
#                     width=512,
#                     height=512)


# result.image


import os
from runware import Runware, IImageInference
import time
import asyncio

async def f():
  runware = Runware(api_key=os.getenv('RUNWARE_API_KEY'))
  await (runware.connect())

  request_image = IImageInference(
    positivePrompt="strong cat",
    #model="runware:100@1",
    model="civitai:36520@76907",
    numberResults=1,
    height=512,
    width=512,
    steps=30
  )

  print("generating..")
  images = await runware.imageInference(requestImage=request_image)
  return images[0].imageURL

loop = asyncio.get_event_loop()
print(loop.run_until_complete(loop.create_task(f())))