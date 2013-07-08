REST API:

List all groups:
GET /groups 

Get group details:
GET /groups/<id>

Add a new group:
POST /groups

Change a group (parameters are optional, but at least to do something useful):
PUT /groups/<id>?level=<level>&name=<name>&channels=<channels>

Delete a group:
DELETE /groups/<id>
