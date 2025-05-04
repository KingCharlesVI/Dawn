package preset

import (
	"encoding/json"
	"io/ioutil"
	"log"
	"net/http"
	"os"
)

type CustomApp struct {
	Name string `json:"name"`
	URL  string `json:"url"`
}

type Preset struct {
	Name       string      `json:"name"`
	Version    string      `json:"version"`
	Apps       []string    `json:"apps"`
	CustomApps []CustomApp `json:"custom_apps,omitempty"`
}

func LoadLocal(name string) Preset {
	data, err := os.ReadFile("presets/" + name + ".json")
	if err != nil {
		log.Fatalf("Failed to load local preset: %v", err)
	}
	var p Preset
	json.Unmarshal(data, &p)
	return p
}

func LoadRemote(url string) Preset {
	resp, err := http.Get(url)
	if err != nil {
		log.Fatalf("Failed to fetch preset from URL: %v", err)
	}
	defer resp.Body.Close()
	body, _ := ioutil.ReadAll(resp.Body)

	var p Preset
	json.Unmarshal(body, &p)
	return p
}
