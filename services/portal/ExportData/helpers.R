## Author: Nasim Gh. 
## email: n-ghazan@nmsu.edu

#install.packages("jsonlite", repos="http://cran.r-project.org")
#install.packages('googleVis')

library(jsonlite)
library(googleVis)
library(httr)
library(shiny)
library(plyr)
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

#Reads land cover data for recorder name
#############################
getLandCoverData<- function(recorder){

  recorderRep <- sub("@", "%40", recorder)
  
  request <- GET(paste0("https://silicon-bivouac-496.appspot.com/_ah/api/transectendpoint/v1/transect?otherUser=",recorderRep),
             config(token = google_token))
  stop_for_status(request)
  cover_data<-content(request,as = "text")
  
  cover_data <- fromJSON(cover_data)
  cover_data <- cover_data$items
  
  if(is.null(cover_data))
  {
    return (NULL)
  }
  
  cover_data<- getCoverData(recorder,cover_data)
  
  print(paste(recorder,nrow(cover_data),"*****",ncol(cover_data)))

  return (cover_data)
  
}


###########################
### returns the column value in df and null if not included
getColumn<-function(df, colname){
  if(colname %in% names(df)){
    return (df[,colname])
  } else {
    return ("")
  }
}


##Calculates and addes the formulas at the end of csv file
#############################
calcFormulas<-function(df){
  names<- unique(df$name)
     
  for(i in 1:length(names) ){
    rowNo <- (i-1)*20 +1
    plot <-subset(df,name == names[i])
    
    plot_total_bare_ground <- sum( plot$bare_total)
    df[rowNo, "plot_total_cover"] <- 100 - plot_total_bare_ground
    df[rowNo, "plot_total_bare_ground"]<- plot_total_bare_ground
    df[rowNo, "plot_total_foliar_cover"] <- sum( plot$trees_total + plot$shrubs_total + plot$sub_shrubs_total + plot$perennial_grasses_total + plot$annuals_total )

    df[rowNo,"plot_total_plant_cover/composition_tree"] <- sum(plot$trees_total)
    df[rowNo,"plot_total_plant_cover/composition_shrub"]<- sum(plot$shrubs_total)
    df[rowNo,"plot_total_plant_cover/composition_sub_shrub"] <- sum(plot$sub_shrubs_total)
    df[rowNo,"plot_total_plant_cover/composition_perennial_grasses"] <-  sum(plot$perennial_grasses_total)
    df[rowNo,"plot_total_plant_cover/composition_annuals"] <-  sum(plot$annuals_total)
    df[rowNo,"plot_total_plant_cover/composition_herb_litter"] <- sum(plot$herb_litter_total)
    df[rowNo,"plot_total_plant_cover/composition_wood_litter"] <- sum(plot$wood_litter_total)
    df[rowNo,"plot_total_plant_cover/composition_rock"] <- sum(plot$rock_total)
    
    
    df[rowNo,"plot_total_canopy_height_smaller_10_cm"] <- nrow(subset(plot,canopy_height=="<10cm")) *5
    df[rowNo,"plot_total_canopy_height_10_50_cm"] <- nrow(subset(plot,canopy_height=="10-50cm")) *5
    df[rowNo,"plot_total_canopy_height_50cm_1m"]	<- nrow(subset(plot,canopy_height=="50cm-1m")) *5
    df[rowNo,"plot_total_canopy_height_1m_2m"]	<- nrow(subset(plot,canopy_height=="1-2m")) *5
    df[rowNo,"plot_total_canopy_height_2m_3m"]	<- nrow(subset(plot,canopy_height=="2-3m")) *5
    df[rowNo,"plot_total_canopy_height_greater_3m"] <- nrow(subset(plot,canopy_height==">3m")) *5
    
    df[rowNo,"plot_total_canopy_gap_percentage"] <- sum(plot$canopy_gap)*5 
    df[rowNo,"plot_total_basal_gap_percentage"] <- sum(plot$basal_gap)*5
    
  }
  return (df)
}

#############################
##reads the landCover data from GAE and return in format
getCoverData<-function(userName,items){
  
  result <<-  data.frame(matrix(ncol = 48, nrow = 0))
  
  colnames(result) <- c("name", "date", 
                        "dominant_woody_species","dominant_nonwoody_species",
                        "transect",  "segment"	,"canopy_height",	"canopy_gap",	"basal_gap",	
                        "stick_segment_1","stick_segment_2",	"stick_segment_3",	"stick_segment_4",	"stick_segment_5",
                        "bare_total",  "trees_total",	"shrubs_total",	"sub_shrubs_total",	"perennial_grasses_total",	"annuals_total"	,"herb_litter_total",	"wood_litter_total",	"rock_total",
                        "plot_total_cover",  "plot_total_bare_ground",	"plot_total_foliar_cover",
                        "plot_total_plant_cover/composition_tree",	"plot_total_plant_cover/composition_shrub",	"plot_total_plant_cover/composition_sub_shrub",	"plot_total_plant_cover/composition_perennial_grasses",	"plot_total_plant_cover/composition_annuals","plot_total_plant_cover/composition_herb_litter",	"plot_total_plant_cover/composition_wood_litter",	"plot_total_plant_cover/composition_rock"	,
                        "plot_total_canopy_height_smaller_10_cm",	"plot_total_canopy_height_10_50_cm",	"plot_total_canopy_height_50cm_1m",	"plot_total_canopy_height_1m_2m",	"plot_total_canopy_height_2m_3m",	"plot_total_canopy_height_greater_3m"	,
                        "plot_total_canopy_gap_percentage"	,"plot_total_basal_gap_percentage",
                        "species_of_interest_1", "species_of_interest_1_count", "species_of_interest_1_density",
                        "species_of_interest_2", "species_of_interest_2_count", "species_of_interest_2_density"
                        )
  
  coverList<- c("Bare","Trees","Shrubs","Sub-shrubs","Perennial grasses","Annuals","Herb litter","Wood litter","Rock")
  
  for(i in 1:nrow(items)){ 
    item<- items[i,]
    name = gsub(paste0(userName,"-"),"",item["siteID"])
    recorder_name = userName
    transect = item["direction"]
    
    dominant_woody_species  = getColumn(item, "dominantWoodySpecies")
    dominant_nonwoody_species= getColumn(item, "dominantNonwoodySpecies")    
    
    speciesOfInterest1 = getColumn(item, "speciesOfInterest1")
    speciesOfInterest2 = getColumn(item, "speciesOfInterest2")
    
    segments<- as.data.frame(item$segments)

    for( j in 1:nrow(segments)){
      segment <- segments[j,]   
      rowNo <- j +(i-1)*5
      
      result[rowNo,"name"] <- name
      result[rowNo,"date"] = getColumn(segment,"date")
      
      result[rowNo,"dominant_woody_species"] = dominant_woody_species  
      result[rowNo,"dominant_nonwoody_species"] = dominant_nonwoody_species
      
      result[rowNo,"transect"]<- transect
         
      result[rowNo,"segment"] = getColumn(segment,"range")
      
      result[rowNo,"canopy_height"] = getColumn(segment,"canopyHeight")
      result[rowNo,"canopy_gap"] = getColumn(segment,"canopyGap")
      result[rowNo,"basal_gap"] = getColumn(segment,"basalGap")
        
      result[rowNo,"stick_segment_1"] = paste(coverList [unlist(segment$stickSegments[[1]]$covers[1])],collapse = ", ")
      result[rowNo,"stick_segment_2"] = paste(coverList [unlist(segment$stickSegments[[1]]$covers[2])],collapse = ", ")
      result[rowNo,"stick_segment_3"] = paste(coverList [unlist(segment$stickSegments[[1]]$covers[3])],collapse = ", ")
      result[rowNo,"stick_segment_4"] = paste(coverList [unlist(segment$stickSegments[[1]]$covers[4])],collapse = ", ")
      result[rowNo,"stick_segment_5"] = paste(coverList [unlist(segment$stickSegments[[1]]$covers[5])],collapse = ", ")
      
      
      covers <-  do.call(rbind,segment$stickSegments[[1]]$covers)
      
      result[rowNo,"bare_total"] <- length(covers[covers[,1]==TRUE,1])
      result[rowNo,"trees_total"]<- length(covers[covers[,2]==TRUE,2])
      result[rowNo,"shrubs_total"]<- length(covers[covers[,3]==TRUE,3])
      result[rowNo,"sub_shrubs_total"]<- length(covers[covers[,4]==TRUE,4])
      result[rowNo,"perennial_grasses_total"]<- length(covers[covers[,5]==TRUE,5])
      result[rowNo,"annuals_total"]<- length(covers[covers[,6]==TRUE,6])
      result[rowNo,"herb_litter_total"] <- length(covers[covers[,7]==TRUE,7])
      result[rowNo,"wood_litter_total"]<- length(covers[covers[,8]==TRUE,8])
      result[rowNo,"rock_total"]<- length(covers[covers[,9]==TRUE,9])
     
      
      result[rowNo,"species_of_interest_1"] = speciesOfInterest1
      result[rowNo,"species_of_interest_1_count"] = getColumn(segment,"speciesOfInterest1Count")
      result[rowNo,"species_of_interest_1_density"] = getColumn(segment,"species1Density")
   
      result[rowNo,"species_of_interest_2"] = speciesOfInterest2
      result[rowNo,"species_of_interest_2_count"] = getColumn(segment,"speciesOfInterest2Count")
      result[rowNo,"species_of_interest_2_density"] = getColumn(segment,"species2Density")

    }
  } 
  
  return (calcFormulas(result))
  
}


#reads list of plots from GAE
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
  
  
  if(dataType == "Metadata for LandInfo" )
  {
    return (read.csv("./Export_METADATA_LandInfo.csv"))
  }
  if(dataType =="Metadata for LandCover")
  { 
    return (read.csv("./Export_METADATA_LandCover.csv"))   
  }
          
  plotData <-getPlotListData()
  
  if(dataType == "LandInfo"){ 
    if(recorder !="all"){
      plotData <- plotData[plotData$recName==recorder ,]
    }
    
    return (plotData)
  }
  
  if(dataType == "LandCover"){
    if(recorder =="all"){
      recorder<-  unique(plotData$recName)
    }
    
    coverData <- NULL
    for(rec in recorder){
      data <- getLandCoverData(rec)
      
      if(!is.null(data)){
        
      if(is.null (coverData )){
        
        coverData = data
      }
      else
        coverData <- rbind.fill(data,coverData)
    
      }
    }
    
    return (coverData)
  }
  
  
  
  return (NULL)
  # req_data$recName <- NULL#req_data [,-which(names(req_data) %in% c("recName"))]     
}

