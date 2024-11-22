from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

# Cria uma instância do Flask
app = Flask(__name__)

# Cria uma instância da API Flask-RESTful
api = Api(app)

# Configura o banco de dados (SQLite, usando um arquivo 'database.db')
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'

# Cria uma instância do SQLAlchemy
db = SQLAlchemy(app)

# Define o modelo VideoModel que será usado para interagir com a tabela de vídeos no banco de dados
class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Campo id, que é a chave primária
    name = db.Column(db.String(100), nullable=False)  # Nome do vídeo
    views = db.Column(db.Integer, nullable=False)  # Número de visualizações
    likes = db.Column(db.Integer, nullable=False)  # Número de curtidas

    def __repr__(self):
        # Representação do objeto VideoModel, que será exibido quando necessário
        return f"Video(name = {self.name}, views = {self.views}, likes = {self.likes})"


# Define o parser para a criação e atualização de vídeos
video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video", required=True)  # Nome do vídeo
video_put_args.add_argument("views", type=int, help="views of the video", required=True)  # Visualizações
video_put_args.add_argument("likes", type=int, help="Likes on the video", required=True)  # Curtidas

# Define o parser para atualizações parciais de vídeos (com argumentos opcionais)
video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of the video")  # Nome do vídeo
video_update_args.add_argument("views", type=int, help="views of the video")  # Visualizações
video_update_args.add_argument("likes", type=int, help="Likes on the video")  # Curtidas

# Define os campos que serão retornados pela API (para formatação da resposta)
resource_fields = {
    'id': fields.Integer,  # Campo id
    'names': fields.String,  # Campo nome
    'views': fields.Integer,  # Campo visualizações
    'likes': fields.Integer,  # Campo curtidas
}


# Define o recurso Video que irá lidar com os endpoints para os vídeos
class Video(Resource):
    # Método GET para retornar informações de um vídeo
    @marshal_with(resource_fields)
    def get(self, video_id):
        # Consulta o vídeo no banco pelo id
        result = VideoModel.query.filter_by(id=video_id).first()

        # Se o vídeo não for encontrado, retorna erro 404
        if not result:
            abort(404, message="Video not found")

        # Se encontrado, retorna o vídeo encontrado
        return result

    # Método PUT para criar um novo vídeo
    @marshal_with(resource_fields)
    def put(self, video_id):
        # Faz o parsing dos argumentos enviados na requisição
        args = video_put_args.parse_args()

        # Verifica se já existe um vídeo com o mesmo id
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message="Video id already exists...")  # Retorna erro 409 se já existir o vídeo com o mesmo id

        # Cria uma nova instância de VideoModel e a adiciona no banco de dados
        video = VideoModel(id=video_id, name=args["name"], views=args["views"], likes=args["likes"])
        db.session.add(video)  # Adiciona o vídeo à sessão
        db.session.commit()  # Comita (salva) a transação no banco de dados

        # Retorna o vídeo criado com o status 201 (Criado com sucesso)
        return video, 201

    # Método PATCH para atualizar parcialmente um vídeo existente
    @marshal_with(resource_fields)
    def patch(self, video_id):
        # Faz o parsing dos argumentos de atualização
        args = video_update_args.parse_args()

        # Consulta o vídeo no banco pelo id
        result = VideoModel.query.filter_by(id=video_id).first()

        # Se o vídeo não for encontrado, retorna erro 404
        if not result:
            abort(404, message="Video doesn't exist, cannot update")

        # Atualiza os campos conforme os argumentos enviados na requisição
        if args["name"]:
            result.name = args["name"]
        if args["views"]:
            result.views = args["views"]
        if args["likes"]:
            result.likes = args["likes"]

        # Comita as mudanças no banco de dados
        db.session.commit()

        # Retorna o vídeo atualizado
        return result

    # Método DELETE para excluir um vídeo
    def delete(self, video_id):
        # Consulta o vídeo no banco pelo id
        result = VideoModel.query.filter_by(id=video_id).first()

        # Se o vídeo não for encontrado, retorna erro 404
        if not result:
            abort(404, message="Video not found")

        # Exclui o vídeo encontrado
        db.session.delete(result)
        db.session.commit()  # Comita a exclusão no banco de dados

        # Retorna um status 202 (aceito) para indicar que o vídeo foi excluído com sucesso
        return "", 202


# Define o endpoint "/video/<int:video_id>" para o recurso Video
api.add_resource(Video, "/video/<int:video_id>")

# Inicia o servidor Flask em modo de desenvolvimento (debug)
if __name__ == "__main__":
    app.run(debug=True)
