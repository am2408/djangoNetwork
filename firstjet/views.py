from django.http import JsonResponse
import json
import requests
from myapp.models import Test
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def apiTest(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        action = data.get("action")

        if action == "check":
            database_data = Test.objects.order_by("-id").values("id", "name")

            # Convertit les données de la base de données en format JSON
            database_data_json = list(database_data)

            # Crée la réponse JSON
            response_data = {
                "message": "Données bien mise à jour !",
                "database_data": database_data_json,
            }

            # Retourne une JsonResponse
            return JsonResponse(response_data)

        elif action == "add":
            # Ajoutez la valeur à la base de données
            new_value = Test(name=f"NewVal {Test.objects.count() + 1}")
            new_value.save()
            # Récupère les données de la base de données
            database_data = Test.objects.order_by("-id").values("id", "name")

            # Convertit les données de la base de données en format JSON
            database_data_json = list(database_data)

            # Crée la réponse JSON
            response_data = {
                "message": "Valeur ajoutée avec succès",
                "database_data": database_data_json,
            }

            # Retourne une JsonResponse
            return JsonResponse(response_data)
        elif action == "delete":
            # Obtenez l'ID à supprimer
            delete_id = data.get("id")

            if delete_id:
                try:
                    # Essayez de récupérer l'enregistrement par son ID
                    record_to_delete = Test.objects.get(id=delete_id)
                    # Supprimez l'enregistrement
                    record_to_delete.delete()

                    # Récupère les données de la base de données après la suppression
                    database_data = Test.objects.order_by("-id").values("id", "name")
                    database_data_json = list(database_data)

                    # Crée la réponse JSON
                    response_data = {
                        "message": f"Enregistrement avec l'ID {delete_id} supprimé avec succès",
                        "database_data": database_data_json,
                    }
                    return JsonResponse(response_data)
                except Test.DoesNotExist:
                    response_data = {
                        "error": f"Aucun enregistrement avec l'ID {delete_id}"
                    }
            else:
                # Obtenez le dernier enregistrement
                last_record = Test.objects.last()

                if last_record:
                    # Supprimez le dernier enregistrement
                    last_record.delete()

                    # Récupère les données de la base de données après la suppression
                    database_data = Test.objects.order_by("-id").values("id", "name")
                    database_data_json = list(database_data)

                    # Crée la réponse JSON
                    response_data = {
                        "message": "Dernier enregistrement supprimé avec succès",
                        "database_data": database_data_json,
                    }
                else:
                    response_data = {"error": "Aucun enregistrement à supprimer"}

                return JsonResponse(response_data)
        elif action == "apiCheck":
            # Remplacez l'URL par l'URL réelle de votre API
            base_url = "http://192.168.0.211/objenious/"

            # Endpoint que vous souhaitez tester
            endpoint = "/objenious/"

            # URL complète pour la requête
            url = base_url

            # Paramètres que vous souhaitez envoyer dans la requête POST
            data = {
                "function": "list",
            }

            # Exemple de requête POST avec des paramètres
            response_api = requests.post(url, data=data)

            # Affiche la réponse
            print(f"Status Code: {response_api.status_code}")
            print("Response Body:")
            print(response_api.text)

            # Récupère les données de la base de données
            database_data = Test.objects.order_by("-id").values("id", "name")

            # Convertit les données de la base de données en format JSON
            database_data_json = list(database_data)

            # Crée la réponse JSON
            response_data = {
                # "api_response": json.loads(response_api.text),
                "api_response": response_api.text,
                "database_data": database_data_json,
            }

            # Retourne une JsonResponse
            return JsonResponse(response_data)
        elif action == "open":
            openedId = data.get("id")

            # Récupère les données de la base de données pour l'ID spécifié
            try:
                record = Test.objects.get(id=openedId)
                # Convertit les données du modèle en un dictionnaire JSON
                database_data_json = {
                    "id": record.id,
                    "name": record.name,
                    # Ajoutez d'autres champs si nécessaire
                }

                # Crée la réponse JSON
                response_data = {
                    "message": "Donnée trouvée avec succès",
                    "database_data": database_data_json,
                }

                # Retourne une JsonResponse
                return JsonResponse(response_data)

            except Test.DoesNotExist:
                # Gérer le cas où l'enregistrement avec l'ID spécifié n'est pas trouvé
                response_data = {
                    "message": "Enregistrement non trouvé pour l'ID spécifié",
                    "database_data": None,
                }
                return JsonResponse(response_data, status=404)
        elif action == "modif":
            openedId = data.get("id")
            new_name = data.get("name")

            # Récupère les données de la base de données pour l'ID spécifié
            try:
                # Récupère l'objet à modifier
                record = Test.objects.get(id=openedId)

                # Vérifie si un enregistrement avec la nouvelle valeur existe déjà
                if Test.objects.filter(name=new_name).exclude(id=openedId).exists():
                    # Si la valeur existe déjà, renvoie une erreur
                    database_data = Test.objects.order_by("-id").values("id", "name")

                    # Convertit les données de la base de données en format JSON
                    database_data_json = list(database_data)
                    response_data = {
                        "error": "La valeur existe déjà dans la base de données",
                        "database_data": database_data_json,
                    }
                    return JsonResponse(response_data)

                # Met à jour la valeur du champ 'name'
                record.name = new_name
                record.save()

                database_data = Test.objects.order_by("-id").values("id", "name")

                # Convertit les données de la base de données en format JSON
                database_data_json = list(database_data)

                # Crée la réponse JSON
                response_data = {
                    "message": "Donnée modifiée avec succès",
                    "database_data": database_data_json,
                }

                # Retourne une JsonResponse
                return JsonResponse(response_data)

            except Test.DoesNotExist:
                # Gérer le cas où l'enregistrement avec l'ID spécifié n'est pas trouvé
                response_data = {
                    "message": "Enregistrement non trouvé pour l'ID spécifié",
                    "database_data": None,
                }
                return JsonResponse(response_data, status=404)
        else:
            return JsonResponse({"error": "Action non prise en charge"})
    else:
        return JsonResponse({"message": "Hello world"})
