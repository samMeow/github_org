from ..instances import db, ma

class GithubOrg(db.BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    github_id = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(256), index=True)

class GithubOrgSchema(ma.BaseSchema):
    id = ma.Int()
    github_id = ma.Int()
    name = ma.String()