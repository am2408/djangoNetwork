from django.http import HttpResponse
import requests


def apiTest(request):
    # Remplacez l'URL par l'URL réelle de votre API
    base_url = "http://192.168.0.211/objenious/"

    # Endpoint que vous souhaitez tester
    endpoint = "/objenious/"

    # URL complète pour la requête
    url = base_url

    # Paramètres que vous souhaitez envoyer dans la requête POST
    # data = {"function": "list"}
    data = {
        "function": "ListOfCountryNamesByCode",
    }

    # Exemple de requête POST avec des paramètres
    response = requests.post(url, data=data)
    # response = requests.get(url)

    # Affiche la réponse
    print(f"Status Code: {response.status_code}")
    print("Response Body:")
    print(response.text)

    # Retourne une HttpResponse avec le contenu de la réponse de la requête
    return HttpResponse(response.text, content_type="application/json")
