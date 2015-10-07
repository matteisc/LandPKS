## Author: Nasim Gh. 
## email: n-ghazan@nmsu.edu

# server.R
source('helpers.R')
library(shiny)
library(googleVis)

shinyServer(function(input, output,session) {


  
  output$downloadData <- downloadHandler(  
    filename = function() { 
      if(input$dataType == "LandInfo"){
        paste('Export_LandInfo_Data', '.csv', sep='') 
      }
      else if(input$dataType == "LandCover")
       {
        paste('Export_LandCover_Data', '.csv', sep='') 
      }
      else if(input$dataType == "Methadata for LandInfo" )
      {
        paste('Export_METADATA_LandInfo', '.csv', sep='') 
      }
      else if(input$dataType == "Methadata for LandCover" )
      {
        paste('Export_METADATA_LandCover', '.csv', sep='') 
      }
      else
        "dummy.csv"
      },
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

