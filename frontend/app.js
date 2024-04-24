const express = require("express");
const cors = require("cors");
const path = require("path");
// const {scrapeWebsite} = require("./scrape.js")

const app = express();
const port = 3000;

app.use(cors());
app.use(express.static(path.join(__dirname, "public")));
app.use(express.json());

app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "./index.html"));
});
app.post("/", (req, res) => {
  res.json(req.body);
});

app.get("/data", (req, res) => {
  res.json("Hello from Express server!");
});

app.post("/data", (req, res) => {
  const requestData = req.body.month;
  console.log("Data received:", requestData);
  res.json(requestData);
});

app.get("/flights", async (req, res) => {
  try {
    const request = {
      trip: 2,
      dep_location_codes: "TPE",
      arr_location_codes: "TYO",
      dep_location_types: 2,
      arr_location_types: 2,
      dep_dates: "2024-05-01",
      return_date: "2024-05-01",
      adult: 1,
      child: 0,
      cabin_class: 2,
      is_direct_flight_only: false,
      exclude_budget_airline: false,
      search_key: "26f232d3205cebfde9db515b67b88b15f21aa1b6",
      target_page: 1,
      order_by: "0_1",
    };

    const params = new URLSearchParams(request).toString();
    console.log(params);
    const url = `https://www.travel4u.com.tw/flight/search/flights/?${params}`;
    const response = await fetch(url);
    const data = await response.json();
    res.json(data);
  } catch (error) {
    console.error("Error fetching data:", error);
    res.status(500).json({ error: "Internal Server Error" });
  }
});

app.post("/flights", async (req, res) => {
  try {
    const requestData = req.body; // Access the entire request body
    const params = new URLSearchParams(requestData).toString();
    const url = `https://www.travel4u.com.tw/flight/search/flights/?${params}`;
    // const url = `https://flight.eztravel.com.tw/tickets-roundtrip-${requestData.depa}-${requestData.dest}/?outbounddate=${requestData.OUT_DATE}&inbounddate=${requestData.IN_DATE}&dport=&aport=&adults=${requestData.adults}&children=0&infants=0&direct=true&cabintype=tourist&airline=&searchbox=t`
    // const url = `https://flight.eztravel.com.tw/tickets-${trip}-${depa}-${dest}/?outbounddate=${OUT_DATE}&inbounddate=${IN_DATE}&dport=&aport=&adults=${adults}&children=0&infants=0&direct=true&cabintype=&airline=&searchbox=s`
    const response = await fetch(url);
    const data = await response.json();
    res.json(data);
  } catch (error) {
    console.error("Error fetching data:", error);
    res.status(500).json({ error: "Internal Server Error" });
  }
});

app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
});
