import uuid
from datetime import datetime
from ..services import util, sqlite, ec2, ecr

def get_status(name):
    query = "SELECT * FROM deployed_repository WHERE repository = ?"
    params = (name,)
    ret = {}
    ret['deployed'] = sqlite.read(query, params, one=True)
    ret['details'] = ecr.describe_repository(name)
    return ret

def set_release(release):
    query = "INSERT INTO deployed_repository (repository, image_tag, released) VALUES (?,?,datetime('now')) ON CONFLICT (repository) DO UPDATE SET image_tag = ?, released = datetime('now')"
    params = (release.repository, release.image, release.image)
    if not sqlite.write(query, params):
        return False
    return True

def instance(id):
    tags = ec2.describe_tags(id)
    repository = ec2._get_tag_value(tags, 'Repository')
    return get_status(repository)

def set_config(repo, config):
    query = "UPDATE deployed_repository SET config = ? WHERE repository = ?"
    params = (config, repo)
    if not sqlite.write(query, params):
        return False
    return True
