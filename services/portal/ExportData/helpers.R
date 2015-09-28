## Author: Nasim Gh. 
## email: n-ghazan@nmsu.edu

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


rowCount <-0

######unlist monthly data columns
convertToDt<-function(col,type){
  df <- data.frame(matrix(ncol = 12, nrow = rowCount))
  if(type == 'min' || type == 'max'){
    colnames(df) <- paste0(type,'_temp_',month.name,' (C)') 
  }
  else
    colnames(df) <- paste0('precipitation_',month.name,' (mm)')  
  
  for(i in 1:rowCount){
    if(! is.null(col[i]))
    {
      df[i,]<-unlist(col[i])
    }
  }
  return (df)
}

########### encrypt email addresses not to be shown fully
obscureEmail<-function(emails){
  i<-1
  result <- NULL
  for(em in emails){
    at<-regexpr("@",em)[1]
    result[i]<-paste0(substr(em,1,3),"********" ,substr(em,at-1,at-1)) 
    i<- i+1
  }
  return (result)
}

############ unlist a list column and paste with a comma
unlistCol<- function(col){
  df <- NULL
  
  for(i in 1:rowCount){
    if(! is.null(col[i]))
    {
      df[i]<- paste(unlist(col[i]),collapse = ", ")
    }
  }
  return (df)
}


###################################
getPlotListData<-function(){
  # 4. Use API
  req <- GET("https://silicon-bivouac-496.appspot.com/_ah/api/plotendpoint/v1/plot?allUsers=true",
             config(token = google_token))
  stop_for_status(req)
  json_data<-content(req,as = "text")
  
  json_data <- fromJSON(json_data)
  json_data <- json_data$items
  
  json_data$obscRecorderName <- obscureEmail(json_data$recorderName)
  json_data$grazingLst <- unlistCol(json_data$grazing)
  
  rowCount <<- nrow(json_data)
  
  csv_data <- subset(json_data, select = c(
    name,recorderName, obscRecorderName, testPlot, latitude,	longitude, modifiedDate,	landCover,	grazed,	grazingLst,	flooding,	slope,	slopeShape,	bedrockDepth,	stoppedDiggingDepth,	
    rockFragmentForSoilHorizon1,
    rockFragmentForSoilHorizon2,	
    rockFragmentForSoilHorizon3,
    rockFragmentForSoilHorizon4,
    rockFragmentForSoilHorizon5,
    rockFragmentForSoilHorizon6,
    rockFragmentForSoilHorizon7,
    textureForSoilHorizon1,
    textureForSoilHorizon2,
    textureForSoilHorizon3,
    textureForSoilHorizon4,
    textureForSoilHorizon5,
    textureForSoilHorizon6,
    textureForSoilHorizon7,
    surfaceCracking,	surfaceSalt,	
    landscapeNorthPhotoURL,
    landscapeEastPhotoURL,	
    landscapeSouthPhotoURL,
    landscapeWestPhotoURL,
    soilPitPhotoURL,
    soilSamplesPhotoURL))
  
    csv_data = cbind(csv_data,convertToDt(json_data$monthlyMaxTemperature,"max"))
    csv_data = cbind(csv_data,convertToDt(json_data$monthlyMinTemperature,"min"))
    csv_data = cbind(csv_data,convertToDt(json_data$monthlyPrecipitation,"prec"))
  
  csv_data <- cbind(csv_data,json_data[ c(
    'averageAnnualPrecipitation',
    'awcSoilProfile',
    'gdalElevation',
    'gdalFaoLgp',
    'gdalAridityIndex')])
  
  
  colnames(csv_data) <- c("name","recName","RecorderName","test_plot","latitude","longitude","modified_date","land_cover","grazed","grazing","flooding","slope","slope_shape","bedrock_depth","stopped_digging_depth",
  "rock_fragment_for_soil_horizon_1","rock_fragment_for_soil_horizon_2","rock_fragment_for_soil_horizon_3","rock_fragment_for_soil_horizon_4","rock_fragment_for_soil_horizon_5","rock_fragment_for_soil_horizon_6","rock_fragment_for_soil_horizon_7",
  "texture_for_soil_horizon_1","texture_for_soil_horizon_2","texture_for_soil_horizon_3","texture_for_soil_horizon_4","texture_for_soil_horizon_5","texture_for_soil_horizon_6","texture_for_soil_horizon_7",
  "surface_cracking","surface_salt",
  "landscape_north_photo_url","landscape_east_photo_url","landscape_south_photo_url","landscape_west_photo_url","soil_pit_photo_url","soil_samples_photo_url",
  "max_temp_January (C)","max_temp_February (C)","max_temp_March (C)","max_temp_April (C)","max_temp_May (C)","max_temp_June (C)","max_temp_July (C)","max_temp_August (C)","max_temp_September (C)","max_temp_October (C)","max_temp_November (C)","max_temp_December (C)",
  "min_temp_January (C)","min_temp_February (C)","min_temp_March (C)","min_temp_April (C)","min_temp_May (C)","min_temp_June (C)","min_temp_July (C)","min_temp_August (C)","min_temp_September (C)","min_temp_October (C)","min_temp_November (C)","min_temp_December (C)",
  "precipitation_January (mm)","precipitation_February (mm)","precipitation_March (mm)","precipitation_April (mm)","precipitation_May (mm)","precipitation_June (mm)","precipitation_July (mm)","precipitation_August (mm)","precipitation_September (mm)","precipitation_October (mm)","precipitation_November (mm)","precipitation_December (mm)",
  "precipitation_annual (mm)","soil_profile_AWC (cm)","Elevation (m)"," FAO Length of Growing Period (days/year)","Aridity Index")
  
  return (csv_data)
}


###########
updateRequestedData<-function(recorder,dataType){
  
  print(recorder)
  
  if(dataType == "LandInfo"){
    
    req_data <-getPlotListData()
    
    if(recorder !="all"){
      req_data <- req_data[req_data$recName==recorder ,]
    }
    
    return (req_data)
  }
  
  return (NULL)
  # req_data$recName <- NULL#req_data [,-which(names(req_data) %in% c("recName"))]     
}

