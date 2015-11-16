## Author: Nasim Gh. 
## email: n-ghazan@nmsu.edu

source('helpers.R')

# server.R

##http://127.0.0.1:6455/?userName=dwkimiti@gmail.com&dataType=LandInfo&allUser=TRUE

shinyServer(function(input, output,session) { 

  observeEvent(TRUE,{
    searchStr = parseQueryString(session$clientData$url_search)
    print(searchStr)
#     
#         shiny::validate(
#           need("userName" %in% names(searchStr) ,'No userName provided!')
#           ,
#           need("dataType" %in% names(searchStr) ,'No dataType provided!')
#           ,
#           need( ( !is.null(searchStr["allUser"]) && searchStr["allUser"]== TRUE) || searchStr["userName"] != "" ,'No user Name provided!')
#         )


    if("allUser" %in% names(searchStr)  && searchStr["allUser"]== TRUE)
    {
      userName<<- "all"  
    }
    else
    {
      userName<<-searchStr["userName"]
    }

    dataType <<-searchStr["dataType"]
      
  })
  
  output$downloadData <- downloadHandler( 

   filename =  function(){
     if(dataType == "LandInfo"){
       'Export_LandInfo_Data.csv' 
     }
     else if(dataType == "LandCover")
     {
       'Export_LandCover_Data.csv' 
     }
     else if(dataType == "MetadataLandInfo" )
     {
       'Export_METADATA_LandInfo.csv'
     }
     else if(dataType == "MetadataLandCover" )
     {
       'Export_METADATA_LandCover.csv'
     }
     else
       "dummy.csv"
     
   },
   content = function(file) { 
     req_data <- updateRequestedData(userName,dataType)
     shinyjs::hide("downloadData")
     if(is.null(req_data) || nrow(req_data) == 0 ){
       stop("No data to display!")
     }
     req_data$recName <- NULL
     write.csv(req_data, file,row.names=FALSE,quote=TRUE,na="",qmethod='escape')

   }
  )
})

