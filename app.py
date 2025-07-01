from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
#import config

app = Flask(__name__)
app.config.from_object(config.Config)
mysql = MySQL(app)

# Rotas básicas
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/search')
def search():
    return render_template('search.html')

# API para buscas estáticas
@app.route('/api/artistas_populares')
def artistas_populares():
    cur = mysql.connection.cursor()
    cur.execute("""
        select Dono as Artista, avg(Popularidade) as mediaPopularidade 
        FROM grava join Musica on Musica_Id = Id
        group by Dono
        order by mediaPopularidade desc
        limit 10;
    """)
    data = cur.fetchall()
    cur.close()
    artists = [{'nome': row[0], 'popularidade': row[1]} for row in data] # fazer isso nas outras querys
    return jsonify(artists)

@app.route('/api/albuns_playlist')
def artistas_populares():
    cur = mysql.connection.cursor()
    cur.execute("""
        select playlist.Nome, count(distinct album.Nome) as qtd
        from playlist join faz_parte on playlist.Id = Playlist_Id join musica on Musica_Id = musica.Id join album on Album_Id = album.Id
        group by playlist.Nome
        order by qtd desc;
    """)
    data = cur.fetchall()
    cur.close()
    return jsonify(data)

@app.route('/api/generos_playlists')
def generos_playlists():
    cur = mysql.connection.cursor()
    cur.execute("""
        select Genero, count(genero) as qtdGeneros from playlist
        group by genero
        order by qtdGeneros desc;
    """)
    data = cur.fetchall()
    cur.close()
    return jsonify(data)


@app.route('/api/musicas_artistas')
def musicas_artistas():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT musica.Nome as Musica, artista.Nome as Artistas
        FROM musica join grava on musica.Id = Musica_Id join artista on Artista_Id = artista.Id
        WHERE Dono != artista.Nome
        limit 10;
    """)
    data = cur.fetchall()
    cur.close()
    return jsonify(data)

@app.route('/api/popularidade_media') # gi vai fazer dps
def musicas_artistas():
    cur = mysql.connection.cursor()
    cur.execute("""
        select distinct Dono, avg(popularidade) as mediapop
        from musica join grava on musica.Id = grava.Musica_Id 
        group by Dono 
        having mediapop > all (select avg(popularidade) as media
                            from playlist join faz_parte on playlist.Id = Playlist_Id join musica on faz_parte.Musica_Id = musica.Id
                            group by playlist.Id)
        order by mediapop desc;
    """)
    data = cur.fetchall()
    cur.close()
    return jsonify(data)



@app.route('/api/musicas_artistas')
def musicas_artistas():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT musica.Nome as Musica, artista.Nome as Artistas
        FROM musica join grava on musica.Id = Musica_Id join artista on Artista_Id = artista.Id
        WHERE Dono != artista.Nome
        limit 10;
    """)
    data = cur.fetchall()
    cur.close()
    return jsonify(data)


# API para busca
@app.route('/api/buscar_musicas', methods=['GET'])
def buscar_musicas():
    termo = request.args.get('termo', '')

    if not termo:
        return jsonify({"error": "Nome da música é obrigatório"}), 400 # erro de requisição devido ao cliente
    
    cur = mysql.connection.cursor()
    cur.execute("""
        select Playlist.Nome 
        from playlist 
        join faz_parte on playlist.Id = Playlist_Id 
        join musica on Musica_Id = musica.Id
        where musica.Nome like %s;
    """, (f'%{termo}%', f'%{termo}%'))
    data = cur.fetchall()
    cur.close()
    return jsonify(data)

#endpoint = fim da url
@app.route('/api/buscar_artistas', methods=['GET'])
def buscar_artistas():
    termo = request.args.get('termo', '')
    cur = mysql.connection.cursor()
    cur.execute("""
        select Dono, playlist.Nome, count(musica.Id) as qtd
        from grava 
        join musica on grava.Musica_Id = musica.Id 
        join faz_parte on musica.Id = faz_parte.Musica_Id 
        right join playlist on Playlist_Id = playlist.Id
        group by Dono, playlist.Nome
        having Dono like %s
        order by qtd desc;
    """, (f'%{termo}%', f'%{termo}%'))
    data = cur.fetchall()
    cur.close()
    return jsonify(data)

@app.route('/api/albuns_artistas', methods=['GET'])
def albuns_artistas():
    termo = request.args.get('termo', '')
    cur = mysql.connection.cursor()
    cur.execute("""
        select album.Nome
        from album join musica on album.Id = Album_Id join grava on musica.Id = Musica_Id join artista on Artista_Id = artista.Id
        where artista.Nome like '%s';
    """, (f'%{termo}%', f'%{termo}%'))
    data = cur.fetchall()
    cur.close()
    return jsonify(data)


@app.route('/api/albuns_artistas', methods=['GET'])
def albuns_artistas():
    termo = request.args.get('termo', '')
    cur = mysql.connection.cursor()
    cur.execute("""
        select album.Nome
        from album join musica on album.Id = Album_Id join grava on musica.Id = Musica_Id join artista on Artista_Id = artista.Id
        where artista.Nome like '%s';
    """, (f'%{termo}%', f'%{termo}%'))
    data = cur.fetchall()
    cur.close()
    return jsonify(data)



if __name__ == '__main__':
    app.run()