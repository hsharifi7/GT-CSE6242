import http.client
import json
import time
import sys
import collections

#Read data from web
def read350Movies(apiKey):
    movie_ID_name = [] 
    conn = http.client.HTTPSConnection("api.themoviedb.org")
    for i in range(1, 19):
        payload = "{}"
        conn.request("GET", "/3/discover/movie?api_key="+apiKey+"&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page="+str(i)+"&primary_release_year=2018", payload)
        res = conn.getresponse()
        data = res.read()
        jData = json.loads(data.decode("utf-8"))
        for index in range(0, len(jData['results'])):
            movie_ID_name.append([ jData['results'][index]['id'],  jData['results'][index]['original_title'] ])
        #print(movie_ID_name)
    conn.close()
    return movie_ID_name

#Read the similar movies
def find5SimilarMovies(apiKey, movie_ID_name): 
    
    movie_ID_sim_movie_ID = {} #Empty dictionary
    movie_ID_sim_movie_ID_list = []
    conn = http.client.HTTPSConnection("api.themoviedb.org")
    count = 0;
    for i in range(0, len(movie_ID_name)) :
    
        count=count+1 
        #if (count==3) : return movie_ID_sim_movie_ID_list
        if count%40 == 0: time.sleep(10)
            
        payload = "{}"
        conn.request("GET", "/3/movie/"+str(movie_ID_name[i][0])+"/similar?page=1&language=en-US&api_key="+apiKey, payload)
        res = conn.getresponse()
        data = res.read()
        jData = json.loads(data.decode("utf-8"))

        for index in range(0, len(jData['results'])):
            key = frozenset([movie_ID_name[i][0], jData['results'][index]['id']])
            if key not in movie_ID_sim_movie_ID:
                movie_ID_sim_movie_ID[key] = [movie_ID_name[i][0], jData['results'][index]['id']]
                movie_ID_sim_movie_ID_list.append([movie_ID_name[i][0], jData['results'][index]['id']])
                       
            if index==4: break;
    
    conn.close()
    return movie_ID_sim_movie_ID_list

def main():
    args =  sys.argv[1:]
    if not args:
        print('usage: python3 script.py <API_KEY>')
        sys.exit(1)
    apiKey = args[0]
    
    #########Reading data from web###########
    movie_ID_name = read350Movies(apiKey)

    ############Writing to file##############
    movie_ID_name_file = open('./movie_ID_name.csv', 'w')
    #movie_ID_name_file.write("movie-ID,movie-name\n");
    for i in range(0, len(movie_ID_name)):
        movie_ID_name_file.write(str(movie_ID_name[i][0])+","+movie_ID_name[i][1]+"\n")

    movie_ID_name_file.close()
    
    #########Reading data from web###########
    time.sleep(10)
    movie_ID_sim_movie_ID = find5SimilarMovies(apiKey, movie_ID_name)
    
    ############Writing to file##############
    movie_ID_sim_movie_ID_file = open('./movie_ID_sim_movie_ID.csv', 'w')
    #movie_ID_sim_movie_ID_file.write("movie-ID,similar-movie-ID\n");
    for i in range(0, len(movie_ID_sim_movie_ID)):
        movie_ID_sim_movie_ID_file.write(str(movie_ID_sim_movie_ID[i][0])+","+str(movie_ID_sim_movie_ID[i][1])+"\n")

    movie_ID_sim_movie_ID_file.close()

############################################
if __name__ == '__main__':
    main()
