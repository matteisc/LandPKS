library(RCurl)
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



## Height class names
hClasses <<- c("<10cm", "10-50cm", "50cm-1m", "1-2m", "2-3m", ">3m")
coverClasses<<- c("trees_total","shrubs_total",  "sub_shrubs_total",  "perennial_grasses_total",	"annuals_total")
foliarList<-c("Trees", "Shrubs", "Sub-shrubs", "Perennial grasses", "Annuals")

plotNames <<- list()

data <- data.frame()


## this method buils the structure of the data
BuildDataFrame <- function() {
  
  ## count of plots
  plotCount <- length(plotNames)
  
  ## build new data frame
  formattedData <- data.frame(matrix(ncol = plotCount, nrow = 23))
  
  ## prepare list of properties
  propertyList = c("Bare Ground%", "Cover%", "", "Canopy gap%", "Basal gap %", 
                   " ", "Species 1", "Species 2", 
                   "Height.class", "<10cm", "10-50cm", "50cm-1m", "1-2m", "2-3m", ">3m" , 
                   "Plant Cover/Composition","trees_total","shrubs_total",  "sub_shrubs_total",	"perennial_grasses_total",	"annuals_total",
                   "  ","Foliar Cover")
  
  # set the property names
  row.names(formattedData) <- propertyList
  
  
  # set plotnames to columns
  colnames(formattedData)[1:plotCount] <- plotNames
  
  return(formattedData)
}

## This method fills the data into data frame

fillDataFrame <- function(df) {
  
  
  for (plot in plotNames) {
    ## fill bare ground data
    df["Bare Ground%", plot] = sum(subset(data, subset = (name == plot), 
                                          select = stick_segment_1:stick_segment_5) == "Bare")
    df["Cover%", plot] = sum(subset(data, subset = (name == plot), 
                                        select = stick_segment_1:stick_segment_5) != "Bare")
    
    ## fill species data
    df["Species 1", plot] = sum(subset(data, 
                                       subset = (name == plot))$species_1_density)/20
    df["Species 2", plot] = sum(subset(data, 
                                       subset = (name == plot))$species_2_density)/20
    
    ## fill gap data
    df["Canopy gap%", plot] = as.numeric( nrow(subset(data, subset = (as.logical(canopy_gap) & 
                                                                        name == plot)))/20 * 100)
    df["Basal gap %", plot] = as.numeric(nrow(subset(data, subset = (as.logical(basal_gap) & 
                                                                       name == plot)))/20 * 100)
    
    ## fill height class values
    for (class in hClasses) {
      df[class, plot] = nrow(subset(data, subset = (canopy_height == 
                                                      class & name == plot)))/20 * 100
    }
    
    ##formula 4
    sumPlantCover = sum(subset(data, subset = (name == plot),select = trees_total:annuals_total))

    for (class in coverClasses) {
      df[class, plot] = round(sum(subset(data, subset = (name == plot),select = class))/sumPlantCover * 100)
    }
    
    ## formula 3
    df["Foliar Cover", plot] = sumFunc(subset(data, subset = (name == plot), 
                                               select = stick_segment_1:stick_segment_5))
  
  }
  return(df)
}


##This method will convert data to a compatible version for scatter plot
transformData<-function(df)
{
  #Transpose the data
  result<-as.data.frame(t(df))
  
  #add a new column with plot names
  result<-cbind(result,plotNames= rownames(result))
  
  #Delete row names
  rownames(result)<-NULL
  
  #Delete the row with was column names
  result<-result[-which(grepl("names",result$plotNames)),]
   
  return (result)
}

convertToNumeric<-function(data){
  #convert two percentage columns to numeric
  
  for(col in names(data))
  {
    if(col !="plotNames")
    {
      data[,col]<- as.numeric(as.character(data[,col]))
    }
  }
  return (data)
}

#returns coverage data
getCoverage<-function(input)
{
  coverageData <- data[c("Bare Ground%", "Cover%"), ]
  coverageData<-convertToNumeric(transformData(coverageData))
  coverageData<-coverageData[coverageData$plotNames %in% input,]
  return (coverageData)
}


#returns gap data
getGap<-function(input)
{
  gapData <- data[c("Canopy gap%", "Basal gap %"), ]
  gapData<-convertToNumeric(transformData(gapData))
  gapData<-gapData[gapData$plotNames %in% input,]
  return (gapData)
 
}

#returns height class data
getHeight<-function(input)
{
  heightData <- data[hClasses, ]
  heightData<-convertToNumeric(transformData(heightData))
  heightData<-heightData[heightData$plotNames %in% input,]
  return (heightData)
  
}

#returns plant cover data
getPlantCover<-function(input)
{
  plantCoverData <- data[coverClasses, ]
  plantCoverData<-convertToNumeric(transformData(plantCoverData))
  plantCoverData<-plantCoverData[plantCoverData$plotNames %in% input,]
  return (plantCoverData)
  
}

#returns species data
getSpecies<-function(input)
{
  speciesData <- data[c("Species 1", 
                        "Species 2"), ]
  
  speciesData<-convertToNumeric(transformData(speciesData))
  speciesData<-speciesData[speciesData$plotNames %in% input,]
  return (speciesData)
  
}

# #returns Foliar Cover data
getFoliar<-function(input)
{
  foliarData<<- data["Foliar Cover", ]
  foliarData<-convertToNumeric(transformData(foliarData))
  foliarData<-foliarData[plotNames %in% input,]
  
  return (foliarData)  
}

#Formula 3
countFunc<-function(x)
{
  x<-as.character(x)
  x<-gsub(" ","",x)
  if(length(intersect(strsplit(x,",")[[1]] , foliarList))>0)
  {
    return (1)
  }
  else
  {
    return (0)
  }
}

sumFunc<-function(df)
{
  return(
      sum(apply(df[1],1,countFunc))+
      sum(apply(df[2],1,countFunc))+
      sum(apply(df[3],1,countFunc))+
      sum(apply(df[4],1,countFunc))+
      sum(apply(df[5],1,countFunc))
  )
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



#############################
##reads the landCover data from GAE and return in format
getCoverData<-function(userName,items){
  
  result <<-  data.frame(matrix(ncol = 48, nrow = 0))
  
  colnames(result) <- c("name", "date", 
                        "dominant_woody_species","dominant_nonwoody_species",
                        "transect",  "segment"  ,"canopy_height",	"canopy_gap",	"basal_gap",	
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
  
  return (result)
  
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
  
  rowCount <<- nrow(json_data)
  
  csv_data <- subset(json_data, select = c(
    name,recorderName))
  
  
  colnames(csv_data) <- c("name","recName")
  
  return (csv_data)
}



##get the data frame for landCover
getData<-function(recorder){
  
  if(recorder =="all"){
    plotData <-getPlotListData()
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
prepareData<-function(recorder )
{ 

  
  data<<-getData(recorder)
  if( is.null(data) || nrow(data) ==0) 
  {
    stop("There is no LandCover data for this user to display!")
  }
  ## extract plot names
  plotNames <<- levels(factor(data, levels = unique(data$name)))
  
  data <<- fillDataFrame(BuildDataFrame())
  
  data$names <<- rownames(data)
    
  
}


