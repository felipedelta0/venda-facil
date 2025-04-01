package main

import (
	"flag"
	"log"
	"vendaFacil/api/routes"

	"github.com/gin-gonic/gin"
)

func main() {
	port := flag.String("port", "8080", "porta para rodar a aplicação")
	flag.Parse()

	router := gin.Default()

	routes.SetupRoutes(router)

	log.Printf("Servidor rodando na porta %s...", *port)
	if err := router.Run(":" + *port); err != nil {
		log.Fatal("Erro ao iniciar o servidor:", err)
	}
}
