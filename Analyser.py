def pstAnalyserPy(fileName):
  import sys
  import pypff
  import os
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
 def printPst(folderName):
  import pandas as pd
  import os
  root = folderName
  sub_folders = os.listdir(root)
  if sub_folders == 0:
    return
  tab_space = "\t"
  print(root)
  for file in sub_folders:
    file_dir = root+"/"+file
    print(tab_space+" - " + file)
    df = pd.read_csv(file_dir)
    for index,row in df.iterrows():
      print(tab_space*2 +" - "+ "Sender : "+row['sender']+" | Subject : "+row['subject'])
