import requests
import json

from API.AFTONBLADET.article import Article

class Aftonbladet:

    """
    ### Aftonbladet.se API

    #### Methods :

    change_quantity(value:int)
    :param: value = integer with how many articles wanted


    """

    def __init__(self) -> None:
        """ Constructor with API url and header, no params"""
        self.api_url = "https://www.aftonbladet.se/frontpage-api/myfeed?subscriber=false&fresh"
        self.headers = {
            "accept-encoding": "gzip, deflate, br",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
        }
        self.article_quantity = 5
        self.counter = 0

    def loop_articles(self) -> list[str]:
        """ Loops through every article from API, creates Article objects
        and returns array with 'self.article_quantity' amount of objects/articles  """
        response = requests.get(self.api_url, headers=self.headers)
        data = json.loads(response.text)
        article_list = []
        url = data["items"][0]["source"]
        self.create_article(url)
        """
        for object in data["items"]:
            url = object["source"]
            article = self.create_article(url)
            #article_list.append(article)
            if (len(article_list) >= self.article_quantity):
                break 
        #return article_list
        """

    def testing(self):
        response = requests.get(self.api_url, headers=self.headers)
        data = json.loads(response.text)
        dir_news = []
        for i in range(8):
            url = data["items"][i]["source"]
            dir_news.append(self.test_loop(url))
        return dir_news


    def test_loop(self, url:str):
        response = requests.get(url, headers=self.headers)
        data = json.loads(response.text)
        dic = {"img":[], "txt": []}
        article = self.recursive(data, dic)
        print("\n")
        print(article)
        print("------------------")
        return article

    def recursive(self, data, dic):
        if ("children" in data):
            for child in data["children"]:

                if ("clickTracking" in child and "accessLevel" in child["clickTracking"]["target"] and child["clickTracking"]["target"]["accessLevel"]== "Paid"):
                    print("\nBREAK BECAUSE OF PAID ARTICLE (AFTONBLADET PLUS\n")
                    break

                if ("tapAction" in child):
                    if ("expandedUri" in child["tapAction"]):
                        article_url = child["tapAction"]["expandedUri"]
                        print(f"expandedUri : {article_url}")

                    elif ("uri" in child["tapAction"]):
                        article_url = child["tapAction"]["uri"]
                        print(f"uri : {article_url}")

                if (child["type"] == "image" and child["imageAsset"]["id"] != "play-icon"):
                    # 0 - 18 url sizes
                    size = 3
                    image = child["imageAsset"]["urls"][size]["url"]
                    print(f"image : {image}")
                    dic["img"].append(image) 

                if (child["type"] == "text"):

                    text = child["text"]["value"]

                    text_markup = []
                    if ("markup" in child["text"]):
                        for markup in child["text"]["markup"]:
                            temp_mark_dir = {}
                            if ("type" in markup):
                                temp_mark_dir["type"] = markup["type"]
                            if ("length" in markup):
                                temp_mark_dir["length"] = markup["length"]
                            if ("offset" in markup):
                                temp_mark_dir["offset"] = markup["offset"]
                            if ("color" in markup):
                                temp_mark_dir["color"] = markup["color"]
                            text_markup.append(temp_mark_dir)


                    font_size = child["textStyles"]["fontSize"]
                    font_color = child["textStyles"]["color"]
                    font_weight = "regular"
                    if ("fontWeight" in child["textStyles"]):
                        font_weight = child["textStyles"]["fontWeight"]

                    print(f"text[{font_weight}:{font_size}:{font_color}] : {text}")
                    dic["txt"].append({"size":font_size, "weight":font_weight, "text":text, "markup":text_markup})

                if ("children" in child):
                    dic = self.recursive(child, dic)

            return dic

        else:
            return dic
    
    def create_article(self, url:str) -> Article:
        """ Creates & returns Article of json object"""
        response = requests.get(url, headers=self.headers)
        data = json.loads(response.text)

        extra = None
        article_url = None
        text = ""
        # Change to recursive function???
        # {"children": []}
        if ("children" in data):
            for first_child in data["children"]:
                #if (self.counter >= 5):
                #    break
                print("**** FIRST CHILD ****")
                # {"children": [{"children": []}]}
                if ("children" in first_child):
                    for second_child in first_child["children"]:
                        print("**** SECOND CHILD ****")
                        """ if theres an 'EXTRA' img """
                        if (second_child["type"] == "image"):
                            # 0 - 18 url sizes
                            size = 3
                            extra = second_child["imageAsset"]["urls"][size]["url"]
                            print(f"extra : {extra}")
                        
                        if ("tapAction" in second_child):
                            article_url = second_child["tapAction"]["uri"]
                            print(f"article url : {article_url}")

                        if ("accessibility" in second_child):
                            text = second_child["accessibility"]["label"]
                            print(f"label : {text}")

                        # {"children": [{"children": [{"children": []}]}]}
                        if ("children" in second_child):
                            for third_child in second_child["children"]:
                                print("**** THIRD CHILD ****")
                                if ("children" in third_child):
                                    for fourth_child in third_child["children"]:
                                        print("**** FOURTH CHILD ****")
                                        """ if theres a image """
                                        if (fourth_child["type"] == "image"):
                                            # 0 - 18 url sizes
                                            size = 3
                                            image = fourth_child["imageAsset"]["urls"][size]["url"]
                                            print(f"image : {image}")

                                        if (fourth_child["type"] == "text"):
                                            # 0 - 18 url sizes
                                            size = 3
                                            text = fourth_child["text"]["value"]
                                            print(f"text : {text}")

                                        if ("children" in fourth_child):
                                            for fifth_child in fourth_child["children"]:
                                                print("**** FIFTH CHILD ****")
                                                """ if theres a image """
                                                if (fifth_child["type"] == "image"):
                                                    # 0 - 18 url sizes
                                                    size = 3
                                                    image = fifth_child["imageAsset"]["urls"][size]["url"]
                                                    print(f"image : {image}")

                                                if (fifth_child["type"] == "text"):
                                                    # 0 - 18 url sizes
                                                    size = 3
                                                    text = fifth_child["text"]["value"]
                                                    print(f"text : {text}")


                        print("------------------------")
                self.counter += 1

        return "OBJECT"
        
        # array with "EXTRA" url image {"url", "width", "height"}
        #data["children"][0]["children"]["imageAsset"]["urls"]
        #data["children"][1]["children"]["imageAsset"]["urls"]

    def FOO(self):
        articles = self.loop_articles()

        for a in articles:
            print(f"----------------------------")
            print(f"{a.text}")
            print(f"URL -> {a.url}")

    def get_data1(self):
        url = "https://www.aftonbladet.se/hyper-api/v1/bundle/JQnzvb,GMPd7Q,15vEWW?curateContext=frontpage&sources=top%2Cbundle%2Cbundle&bundleType=manual"
        response = requests.get(url, headers=self.headers)
        with open('/Users/tacobaco/myprojects/MAGIC_MIRROR/API/AFTONBLADET/json_response.json', 'w') as file:
            file.write(response.text)

    def get_data_first_article(self):
        response = requests.get(self.api_url, headers=self.headers)
        data = json.loads(response.text)
        first_article_url = data["items"][2]["source"]
        response = requests.get(first_article_url, headers=self.headers)
        data = json.loads(response.text)
        with open('/Users/tacobaco/myprojects/MAGIC_MIRROR/API/AFTONBLADET/json_response.json', 'w') as file:
            file.write(response.text)