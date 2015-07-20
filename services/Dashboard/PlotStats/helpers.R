## Author: Nasim Gh. 
## email: n-ghazan@nmsu.edu
## 6/24/2015

#install.packages("jsonlite", repos="http://cran.r-project.org")
#install.packages('googleVis')

library(jsonlite)
library(googleVis)
library(httr)
library(shiny)
source('Auth.R')#contains key and secret


# 1. Find OAuth settings for google:
#    https://developers.google.com/accounts/docs/OAuth2InstalledApp
oauth_endpoints("google")

# 2. Register an application at https://cloud.google.com/console#/project
myapp <- oauth_app("google",
                   key = myKey,
                   secret = mySecret)


# 3. Get OAuth credentials
google_token <- oauth2.0_token(oauth_endpoints("google"), myapp,
                               scope = c("https://www.googleapis.com/auth/userinfo.profile","https://www.googleapis.com/auth/userinfo.email"))

# 4. Use API
req <- GET("https://silicon-bivouac-496.appspot.com/_ah/api/plotendpoint/v1/plot?allUsers=true",
           config(token = google_token))
stop_for_status(req)
json_data<-content(req,as = "text")

statMean <<- 0
statMedian <<- 0
statMin <<- 0
statMax <<- 0

### reading from static file
# json_file <- "data/plotList.json"
# json_data <- readChar(json_file, file.info(json_file)$size)

json_data <- fromJSON(json_data )
json_data <- json_data$items
json_data["value"] <-1


json_data$shortdate <- strftime(json_data$modifiedDate, format="%Y/%m")


minDate <- min(json_data$modifiedDate)
maxDate <- max(json_data$modifiedDate)

tmp_agg_data <- aggregate(json_data$value , list(user = json_data$recorderName, time = json_data$shortdate), sum)

minCount<- min(tmp_agg_data$x)
maxCount<- max(tmp_agg_data$x)


userNames <- unique(json_data$recorderName)
userNames <- sort(userNames)

json_agg_data <- aggregate(json_data$value , list(user = json_data$recorderName, time = json_data$shortdate), sum)

months<- unique(json_agg_data$time)

getUserData<-function (userList,dates,count){  
  statMean <<- 0
  statMedian <<- 0
  statMin <<- 0
  statMax <<- 0  
  
  start <- dates[1]
  end <- dates[2]
  
  min <- count[1]
  max <- count[2]
  
  userData <-json_data[json_data$modifiedDate <= end & json_data$modifiedDate >= start,]
  userData <- userData[userData$recorderName  %in% userList ,]
  
  if(nrow(userData) ==0 ) return (NULL)
  
  userData <- aggregate(userData$value , list(user = userData$recorderName, time = userData$shortdate), sum)
  
  userData <- userData[userData$x <= max & userData$x >= min  ,]
  
  if(nrow(userData) ==0 ) return (NULL)
  
  updateStats(userData)
  
  dates<- unique(userData$time)
  emails<- unique(userData$user)
  data <- data.frame(matrix(ncol = length(dates)+1, nrow = length(emails)))
  names(data)[1] <- "recorder" 
  for(i in 1:(length(dates))+1){
    d = dates[i-1]
    
    y = unlist(strsplit(d,"/"))[1]
    m = month.abb[as.numeric(unlist(strsplit(d,"/"))[2])]
    names(data)[i] <-  paste(m,y)
    
  }
  
  for(i in 1: length(emails)){
    data[i,1] <- emails[i]
    for(j in 1:(length(dates))+1){
      count<-  userData[userData$user == emails[i] & userData$time == dates[j-1],3]
      if(length(count) == 0)
        count <- 0
      data[i,j] <- count
    }
  }
  
  data <- cbind(data,sum=rowSums(data[2:ncol(data)]))
  data <- data[order(-data$sum),]
  data$sum<-NULL
  
  return (data)
}

updateStats<- function (userData){
  
  statMean <<- round(mean(userData$x),digits = 2)
  statMedian <<- median(userData$x)
  statMin <<- min(userData$x)
  statMax <<- max(userData$x)
}
# getTransposeData<-function (userList){
#   data<- getUserData(userList)
#   data<- as.data.frame(t(data))
#   names(data) = as.character(unlist(data[1,]))
#   data<-data[-1,]
#   data[1:length(data)]<-as.numeric(as.character(data)) 
#   return (data)
# }
