def pstAnalyserPy(fileName):
  import pypff
  import sys
  import os
  from collections import Counter
  import argparse
  import pandas as pd
  def processMessage(message):
    return {
        "subject": message.subject,
  "sender": message.sender_name,
  "header": message.transport_headers,
  "body": message.plain_text_body,
  "creation_time": message.creation_time,
  "submit_time": message.client_submit_time,
  "delivery_time": message.delivery_time,
  "attachment_count": message.number_of_attachments,
    }
  def folderReport(msg_list, folder_name):
    if not len(msg_list):
      return
    temp_dict = {}
    for col in msg_list[0]:
      temp_dict[col] = []
    for msg in msg_list:
      for id in msg:
        temp_dict[id].append(msg[id])
    try:
      pd.DataFrame(temp_dict).to_csv(f"{fileName[:-4]}/{folder_name}.csv", index=False)
    except:
      return
  def checkForMessage(folder):
    msg_list = []
    for message in folder.sub_messages:
      msg_dict = processMessage(message)
      msg_list.append(msg_dict)
    folderReport(msg_list,folder.name)

  def folderTraverse(root_base):
    for folder in root_base.sub_folders:
      if folder.number_of_sub_folders:
        folderTraverse(folder)  
      checkForMessage(folder)
  pst = pypff.open(fileName)
  root = pst.get_root_folder()
  try:
    os.mkdir(f"{fileName[:-4]}")
  except:
    return
  folderTraverse(root)
