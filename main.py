import grequests
import requests

def question_1():
    url = "https://pokeapi.co/api/v2/pokemon"
    args = { "limit": "1500" }
    response = requests.get(url, params=args)    
    if response.status_code == 200:
        results = response.json().get("results", [])
        if results:
            pokemons = [pokemon["name"] for pokemon in results]
            return(len(list(filter(lambda x: ("at" in x and x.count("a") == 2), pokemons))))

def question_2():
    url = "https://pokeapi.co/api/v2/pokemon/raichu"
    response = requests.get(url)
    if response.status_code == 200:
        species_url = response.json().get("species").get("url")
        species_response = requests.get(species_url)
        if species_response.status_code == 200:
            eg_results = species_response.json().get("egg_groups")
            eg_urls = [eg["url"] for eg in eg_results]
            pokemons = []
            for url in eg_urls:
                resp = requests.get(url)
                if response.status_code == 200:
                    res = resp.json().get("pokemon_species")
                    pokemons.extend([i["name"] for i in res])
            pokemons = list(set(pokemons))
            return(len(pokemons))

def question_3():
    url = "https://pokeapi.co/api/v2/generation/1/"
    response = requests.get(url) 
    if response.status_code == 200:
        respultsss = response.json().get("types", [])
        fighting_url = list(filter(lambda x: x["name"]=="fighting", respultsss))[0]['url']
        pokemons = requests.get(fighting_url)
        if pokemons.status_code == 200:
            list_of_pokemons = [i["pokemon"] for i in pokemons.json().get("pokemon",)]
            urls = [i["url"] for i in list_of_pokemons]
            reqs = (grequests.get(u) for u in urls)
            responses = grequests.map(reqs)
            responses_ok = filter(lambda x: x.status_code == 200, responses) 
            weights = [i.json().get("weight") for i in responses_ok]
            return([max(weights), min(weights)])

def main():
    while True:
        try:
            msg = "\n\n" \
            "1) Obtén cuantos pokemones poseen en sus nombres “at” y tienen 2 “a” en su nombre, incluyendo la primera del “at” " \
            "La respuesta debe ser un número. \n" \
            "2) ¿Con cuántas especies de pokémon puede procrear raichu? (2 Pokémon pueden procrear" \
            "si están dentro del mismo egg group). La respuesta debe ser un número. Recuerda eliminar los duplicados.\n" \
            "3) Entrega el máximo y mínimo peso de los pokémon de tipo fighting de 1ra generación (cuyo id sea menor o igual a 151)." \
            "La respuesta debe ser una lista con el siguiente formato: [1234, 12], donde 1234 corresponde al máximo peso y 12 al mínimo.\n\n" \
            "Ingresa el número de la pregunta de la cual deseas conocer la respuesta: "
            choice = int(input(msg))
        except ValueError:
            print("Por favor, solo números.")
            continue
        else:     
            break
        
    if choice == 1:
        print(f"\nLa respuesta es: {question_1()}")
    elif choice == 2:
        print(f"\nLa respuesta es: {question_2()}")
    elif choice == 3:
        print(f"\nLa respuesta es: {question_3()}")
    else:
        print("Opción incorrecta, terminando el programa.")

if __name__ == "__main__":
    while True:
        main()
        if input("\n¿Repetir el programa? (Y/N)").strip().upper() != 'Y':
            break