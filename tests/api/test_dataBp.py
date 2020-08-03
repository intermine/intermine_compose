# from io import BytesIO


# def updateUploadFileID(var, fileId):
#     var = fileId

# uploadFileID = ""

# def test_uploadDataFile(client, cookies):
#     client.set_cookie("test_cookie", cookies)
#     # create a dummy file
#     data = {
#         'dataFile': (BytesIO(b'my file contents'), 'test_file.txt'), # we use StringIO to simulate file object
#     }
#     resp = client.post(
#         "/api/v1/data/file/upload/",
#         data=data
#     )
#     assert resp.status_code == 200
#     updateUploadFileID(uploadFileID, resp.data)


# def test_getDataFiles(client, cookies):
#     client.set_cookie("test_cookie", cookies)
#     resp = client.get(
#         "/api/v1/data/files"

#     )
#     assert resp.status_code == 200

# def test_getDataFile(client, cookies):
#     client.set_cookie("test_cookie", cookies)
#     resp = client.get(
#         f"/api/v1/data/file/?fileId={uploadFileID}"
#     )
#     print(uploadFileID)
#     assert resp.status_code == 200

# def test_delDataFile(client, cookies):
#     client.set_cookie("test_cookie", cookies)
#     resp = client.delete(
#         f"/api/v1/data/file/?fileId={uploadFileID}"
#     )
#     print(uploadFileID)
#     assert resp.status_code == 200
