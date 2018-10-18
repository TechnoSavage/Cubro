try {
  $result = invoke-restmethod -method Get -uri "http://192.168.1.220/rest/device/ipconfig?" -ContentType "application/json" -UseBasicParsing | ConvertFrom-Json
}
catch {
  $result = $_.Exception.Response.GetResponseStream()
  $reader = New-Object System.IO.StreamReader($result)
  $reader.BaseStream.Position = 0
  $reader.DiscardBufferedData()
  $responseBody = $reader.ReadToEnd();
}
