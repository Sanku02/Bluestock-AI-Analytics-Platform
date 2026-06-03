import CryptoJS from "crypto-js";


const BASE_URL =
  "http://127.0.0.1:8000/api/partner/v1";


const API_KEY =
  "0282a0c3-70af-4521-a595-90cf54d7a654";


const SECRET =
"a6305a998a2232e8538cd45e5068ea893483693e879c1ff07b877717ec2a6a0a";



function generateHeaders(
  method,
  endpoint
) {

  const timestamp =
    Math.floor(Date.now() / 1000)
      .toString();

  const nonce =
    crypto.randomUUID();

  const message =
  method +
  endpoint +
  timestamp;


  const signature =
    CryptoJS.HmacSHA256(
      message,
      SECRET
    ).toString();


  return {

    "X-API-Key-ID":
      API_KEY,

    "X-Timestamp":
      timestamp,

    "X-Nonce":
      nonce,

    "X-Signature":
      signature,

  };

}



async function apiRequest(
  endpoint,
  method = "GET"
) {

  const response = await fetch(

    BASE_URL + endpoint,

    {

      method,

      headers:
        generateHeaders(
          method,
          "/api/partner/v1" + endpoint
        ),

    }

  );


  if (!response.ok) {

    throw new Error(
      "API request failed"
    );
  }


  return response.json();

}



/* DASHBOARD */

export async function getDashboard() {

  return apiRequest(
    "/dashboard/"
  );
}


/* SECTOR RANKINGS */

export async function getSectorRankings() {

  return apiRequest(
    "/sector-rankings/"
  );
}


/* TOP COMPANIES */

export async function getTopCompanies() {

  return apiRequest(
    "/top-companies/"
  );
}