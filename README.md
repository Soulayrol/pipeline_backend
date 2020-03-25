# Pipeline backend with Rest API

===========================================<br/>
This repo is based on the pipeline_base repo from ArtFx :school:<br/>
https://gitlab.com/artfx-pipeline/pipline_base/-/tree/prod<br/>
===========================================<br/>
### Dependences
Build with Docker<br/>

`flask`==`1.1.1`<br/>
`flask_restful`==`0.3.8`<br/>
`markdown`==`3.1.1`<br/>
`jsonify`==`0.5`<br/>
`logzero`==`1.5.0`<br/>
`lucidity`==`1.5.1`<br/>
`pathlib2`==`2.3.5`<br/>
`gazu`==`0.7.8`<br/>

### Responce from the lib :
```json
{
  "data": "responce with type needed",
  "message": "Error or success return"
}
```
### List all questions
* `Definition` => `Response`

#### Project
* `Get /projects` => 
```json
[ "project1", "project2", "project3" ]
```

#### Sid (Shot and Asset)

##### GET
`shot` => `file/project/s/seq/shot/task/subtask/state/version/ext`<br/>
`asset` => `file/project/a/cat/name/task/subtask/state/version/ext`

Fill the rest request with what you want<br/>
*Exemples :* <br/>
`demo/s/s010/p010/comp/` => return the next comp folder (subtask)<br/>
`demo/s/*/*/*/*/*/*/*/*/` => return all the shot from demo project
###### Asset
* `Get /project_name/assets` =>
```json
[ 
  {
    "project": "asset_project_name",
    "cat": "asset_category",
    "name": "asset_name",
    "task": "asset_task",
    "subtask": "asset_subtask",
    "state": "asset_state",
    "version": "asset_version",
    "ext": "file_scene_extension",
    "date": "file creation date",
    "tag": "tag",
    "comment": "comment"
  },
  {
    "Same for all assets": ""
  }
]
```
###### Shot
* `Get /project_name/shots` =>
```json
[ 
  {
    "project": "shot_project_name",
    "seq": "shot_seq",
    "shot": "shot_shot",
    "task": "shot_task",
    "subtask": "shot_subtask",
    "state": "shot_state",
    "version": "shot_version",
    "ext": "file_scene_extension",
    "date": "file creation date",
    "tag": "tag",
    "comment": "comment"
  },
  {
    "Same for all shots": ""
  }
]
```


##### POST

For create shoot or asset you need :<br/>
**Arguments :** <br/>
###### Shot
- `"project":string` Name of the project
- `"type":string` Type (a for asset, s for shot)
- `"seq":string` Name of the sequence
- `"shot":string` Name of the shot
- `"task":string` Name of the task
- `"subtask":string` Name of the subtask
- `"state":string` State (w=work, p=publish)
- `"version":string` Version (ex: v001)
- `"ext":string` File extension (without ".")
- `"tag":string` Tag can be null
- `"comment":string` Comment can be null

###### Asset
- `"project":string` Name of the project
- `"type":string` Type (a for asset, s for shot)
- `"cat":string` Name of the category
- `"name":string` Asset name
- `"task":string` Name of the task
- `"subtask":string` Name of the subtask
- `"state":string` State (w=work, p=publish)
- `"version":string` Version (ex: v001)
- `"ext":string` File extension (without ".")
- `"tag":string` Tag can be null
- `"comment":string` Comment can be null

**Responce :** <br/>
```json
{
  "data": "true if created, false if not",
  "message": "Message"
}
```