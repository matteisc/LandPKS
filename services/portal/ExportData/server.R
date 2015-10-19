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
      else if(input$dataType == "Metadata for LandInfo" )
      {
        paste('Export_METADATA_LandInfo', '.csv', sep='') 
      }
      else if(input$dataType == "Metadata for LandCover" )
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
  
  isValidEmail <- function(x) {
    grepl("\\<[A-Z0-9._%+-]+@[A-Z0-9.-]+\\.[A-Z]{2,}\\>", as.character(x), ignore.case=TRUE)
  }
  
  updateData<- function(){
    
    recorder <-""
    
    if( input$exportAll )
    {
      recorder = "all"
    }
    else
    {
      if(isValidEmail(input$recorder)){
        recorder <- input$recorder  
      }
      else
      {
        stop("Please enter a valid email address!")
      }
      
    } 
    
    return (updateRequestedData(recorder,input$dataType))
  }
  
  
})

