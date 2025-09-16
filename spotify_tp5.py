
import requests
import base64

CLIENT_ID = '8d7ab6a5639f428a9165b9925c5737e5'
CLIENT_SECRET = '39f15adfc92f47ca91ae37f6e961b766'

def get_access_token(client_id, client_secret):
    """
    Obtiene el token de acceso usando Client Credentials Flow.
    """
    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': 'Basic ' + base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    }
    data = {
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, headers=headers, data=data)
    if response.status_code != 200:
        print("Error al obtener token:", response.text)
        return None
    return response.json().get('access_token')

def get_top_tracks(artist_id, token, market='AR'):
    """
    Consulta los Top Tracks de un artista por su ID.
    """
    url = f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    params = {
        'market': market
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print("Error al obtener Top Tracks:", response.text)
        return None
    return response.json()

def main():
    """
    Función principal: pide ID de artista, obtiene token y muestra Top Tracks.
    """
    print("Programa para consultar los Top Tracks de un artista en Spotify 🎶")
    artist_id = input("👉 Ingresá el ID del artista de Spotify: ").strip()
    token = get_access_token(CLIENT_ID, CLIENT_SECRET)

    if not token:
        print("No se pudo obtener el token de acceso.")
        return

    top_tracks_data = get_top_tracks(artist_id, token)

    if not top_tracks_data or 'tracks' not in top_tracks_data:
        print("No se pudieron obtener los Top Tracks.")
        return

    print("\n Top Tracks del artista:")
    for idx, track in enumerate(top_tracks_data['tracks'], start=1):
        print(f"{idx}. {track['name']} ({track['album']['name']})")

if __name__ == "__main__":
    main()
  