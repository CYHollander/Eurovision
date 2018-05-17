library(shiny)
library(shinydashboard)
library(data.table)
library(dplyr)
library(ggplot2)

evdata= fread(input='eurovision_data.csv')

# Define UI for application that draws a histogram
ui <- dashboardPage(
  
  # Application title
  dashboardHeader(title="Eurovision"),
  dashboardSidebar(
    sidebarUserPanel("C. Y.", image = "Chaim_Yehuda_Hollander.jpg"),
    sidebarMenu(
      menuItem("By Year", tabName = "byyear"),
      menuItem("By Country", tabName = "bycountry")
    )
    ),
    dashboardBody(
      tabItems(tabItem(tabName = "byyear",
      plotOutput("plot1",hover=hoverOpts(id="plot_hover")),
      box(title = "Year",
          selectizeInput(inputId="year",
                         label="Year",
                         choices=(min(evdata$Year):max(evdata$Year))
                        ),
          sliderInput(inputId = "Round",
                      label= "Simulated Runoff Voting",
                      min=1,
                      max=n_distinct(evdata$Country),
                      value=c(1),
                      animate =TRUE)
          ),
      verbatimTextOutput("song_title")),
      
      tabItem(tabName = "bycountry",
              plotOutput("plot2",hover=hoverOpts(id="plot2_hover")),
              box(title="Country",
                  selectizeInput(inputId="country",
                                 label= "Country",
                                 choices=(unique(evdata$Country))
                  )
              ),
              verbatimTextOutput("song_title2")
      ))
    )
)
    #

# Define server logic required to draw a histogram
server <- function(input, output) {
  
  output$plot1 <- renderPlot({
    data = filter(evdata,Year==input$year) %>% 
      select(Year, Country, Song, Language, Place, 
             one_of(sub(' ','',data$Country))) %>% 
      mutate(Place=ifelse(as.numeric(Place)<10,paste0('0',Place),Place)) %>% 
      mutate(Country=paste(Place,Country))
    # generate bins based on input$bins from ui.R
    #data$order <- factor(data$Place)
    ggplot(data,aes(x=Place,y=Country))+geom_point()
  })
  
  output$song_title <- renderPrint({
    data = select(evdata, Year, Country, Place, Song, Language) %>% 
      filter(Year==input$year) %>% 
      mutate(Place=ifelse(as.numeric(Place)<10,paste0('0',Place),Place)) %>% 
      mutate(Country=paste(Place,Country)) %>% 
      arrange(Place)
    
    if(!is.null(input$plot_hover)){
      entry = round(input$plot_hover$y)
      song=paste('Title:',gsub('"','', data$Song[entry]))
      language=paste('Language:',data$Language[entry])
    cat(song,'\n',entry,language,'\n',data$Country[entry])}
    
  })
  
  output$plot2 <- renderPlot({
    data2 = select(evdata, Year, Country, Place) %>% 
      filter(Country==input$country) %>% 
      mutate(Place=ifelse(as.numeric(Place)<10,paste0('0',Place),Place)) %>% 
      arrange(as.numeric(Year))
    #data$order <- factor(data$Place)
    ggplot(data2,aes(x=Year,y=Place))+geom_point()+
      scale_x_continuous(breaks = round(seq(min(data2$Year), max(data2$Year), by = 5),1))
  })
  output$song_title2 <- renderPrint({
    data2 = select(evdata, Year, Country, Place, Song, Language) %>% 
      filter(Year==input$year) %>% 
      mutate(Place=ifelse(as.numeric(Place)<10,paste0('0',Place),Place)) %>% 
      mutate(Country=paste(Place,Country)) %>% 
      arrange(Place)
    
    if(!is.null(input$plot2_hover)){
      entry = round(input$plot2_hover$x)
      song=paste('Title:',gsub('"','', data2$Song[entry]))
      language=paste('Language:',data2$Language[entry])
      #cat(song,'\n',entry,language,'\n',data2$Country[entry])
      cat(entry,' ',round(input$plot2_hover$y))}
    
  })
  
}

# Run the application 
shinyApp(ui = ui, server = server)