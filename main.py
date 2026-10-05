from fastapi import FastAPI

app = FastAPI()


@app.get('/')
async def root():
    return {'status': 'ok'}


@app.post('/watchers')
async def add_watcher():
    pass


@app.get('/watchers')
async def read_watchers():
    pass


@app.update('/watchers')
async def edit_watcher(id):
    pass


@app.delete('/watchers/{id}')
async def delete_watcher(id):
    pass


@app.get('/watchers/{id}')
async def read_watcher(id):
    pass
