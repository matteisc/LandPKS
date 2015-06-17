library(RCurl)


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
                                          select = stick_segment_0:stick_segment_4) == "Bare")
    df["Cover%", plot] = sum(subset(data, subset = (name == plot), 
                                        select = stick_segment_0:stick_segment_4) != "Bare")
    
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
                                               select = stick_segment_0:stick_segment_4))
  
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


prepareData<-function(url)
{ 
  ## read the csv file from GitHub
  # Set SSL certs globally
  options(RCurlOptions = list(cainfo = system.file("CurlSSL", "cacert.pem", package = "RCurl")))

  url<- getURL(url)  
  data<<-read.csv(textConnection(url))
  if(nrow(data) ==0) 
  {
    stop("There is no RHM data for this user to display!")
  }
  ## extract plot names
  plotNames <<- levels(factor(data, levels = unique(data$name)))
  
  data <<- fillDataFrame(BuildDataFrame())
  
  data$names <<- rownames(data)
  

  
  
}


