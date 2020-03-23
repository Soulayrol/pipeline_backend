<h2>Pipeline backend with Rest API</h2>

<p>=============================================</p>
<p>This repo is based on the pipeline_base repo from ArtFx</p>
<a href="https://gitlab.com/artfx-pipeline/pipline_base/-/tree/prod">Go to pipeline_base repo</a>
<p>=============================================</p>
<h4>Dependences</h4>
<p>Flask | Flask-RESTful</p>
<p>jsonify</p>

<h4>Responce from the lib :</h4>
```json
{
  "data": "responce with type needed",
  "message": "Error or success"
}
```
<h4>List all questions</h4>
- `Definition` => `** Response **`
<br/><br/>
- `Get /projects` => 
```json
[ "project1", "project2", "project3" ]
```

<h5>Asset</h5>
- `Get /project_name/assets` =>
```json
[ 
  {
    "project": "asset_project_name",
    "cat": "asset_category",
    "name": "asset_name",
    "task": "asset_task",
    "subtask": "asset_subtask",
    "state": "asset_state",
    "version": "asset_version"
  },
  {
    "Same for all assets": ""
  }
]
```
- `Get /project_name/assets/cat/name/task/subtask/state/version` =>
```json
{
 "tag": "tag",
 "comment": "comment"
}
```

<h5>Shot</h5>
- `Get /project_name/shots` =>
```json
[ 
  {
    "project": "shot_project_name",
    "seq": "shot_seq",
    "shot": "shot_shot",
    "task": "shot_task",
    "subtask": "shot_subtask",
    "state": "shot_state",
    "version": "shot_version"
  },
  {
    "Same for all shots": ""
  }
]
```
- `Get /project_name/shots/seq/shot/task/subtask/state/version` =>
```json
{
 "tag": "tag",
 "comment": "comment"
}
```


