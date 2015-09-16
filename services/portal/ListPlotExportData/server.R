## Author: Nasim Gh. 
## email: n-ghazan@nmsu.edu

# server.R
source('helpers.R')
library(shiny)
library(googleVis)

shinyServer(function(input, output,session) {

  updateData<- function(){

    recorder <-""
    searchStr = parseQueryString(session$clientData$url_search)

    print(searchStr)
    if( ("recorderName" %in% names(searchStr) == F) || is.null(searchStr["recorderName"]) )
      {
      recorder = "all"
    }
    else
     {
       recorder <- searchStr["recorderName"]
     } 
    print(recorder)
    
#     shiny::validate(
#       need("recorderName" %in% names(searchStr) ,'Unavailable1')
#       #,
#      # need(searchStr["recorderName"] != "" ,'Unavailable2')
#     )
    
    updateRequestedData(recorder)
  }
  
  output$downloadData <- downloadHandler(  
    filename = function() { paste('Export_LandInfo_Data', '.csv', sep='') },
    content = function(file) {
      updateData()
      req_data$recName <- NULL
      write.csv(req_data, file,row.names=FALSE,quote=TRUE,na="",qmethod='escape')
    }
  )
})

