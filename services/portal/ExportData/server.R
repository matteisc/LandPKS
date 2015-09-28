## Author: Nasim Gh. 
## email: n-ghazan@nmsu.edu

# server.R
source('helpers.R')
library(shiny)
library(googleVis)

shinyServer(function(input, output,session) {


  
  output$downloadData <- downloadHandler(  
    filename = function() { paste('Export_LandInfo_Data', '.csv', sep='') },
    content = function(file) {     
      req_data <- updateData()
      req_data$recName <- NULL
      write.csv(req_data, file,row.names=FALSE,quote=TRUE,na="",qmethod='escape')
    }
  )
  
  
  updateData<- function(){
    
    recorder <-""
    
    if( input$exportAll )
    {
      recorder = "all"
    }
    else
    {
      recorder <- input$recorder
    } 
    
    return (updateRequestedData(recorder,input$dataType))
  }
  
  
})

