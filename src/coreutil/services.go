package coreutil

import (
	"flag"
)

func Start(v flag.Value) {

	// // Starting hackthebox service

	// // Initializing selenium driver with Chrome
	// _, err := selenium.NewChromeDriverService(filepath.Join(ETC_PATH, "chromedriver"), 4444)
	// if err != nil {
	// 	log.Fatal("ERROR: ", err)
	// }
	// // defer service.Stop()

	// // configure the browser options
	// caps := selenium.Capabilities{}

	// // create a new remote client with the specified options
	// driver, err := selenium.NewRemote(caps, "")
	// if err != nil {
	// 	log.Fatal("ERROR: ", err)
	// }

	// // maximize the current window to avoid responsive rendering
	// err = driver.MaximizeWindow("")
	// if err != nil {
	// 	log.Fatal("ERROR: ", err)
	// }

	// // Connect to the page
	// driver.Get("https://account.hackthebox.com/login")
	// if err != nil {
	// 	log.Fatal("ERROR: ", err)
	// }

	// // Email button
	// // /html/body/div/div/div/main/div[2]/div/div[1]/div/div/div/div/div/form/div[2]/div[1]/div/div[3]/input

	// // Getting the page
	// html, err := driver.PageSource()
	// if err != nil {
	// 	log.Fatal("Error:", err)
	// }
	// fmt.Println(html)

}
