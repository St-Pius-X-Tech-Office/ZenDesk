# ZenDesk

This repo is to house ZenDesk API scripts. So far it is simply used to pull all of the prior
month's data into a csv. 

## Credentials

There is a 'sampleCredentials.json' file in the repo. Simply replace the credentials with your
zendesk login details in order to get a successful call.


### API Limit Workaround

There is a way around the API limit, which at this time is 1000. If you are a busier school, you might
need to call it. Below is a sample code to get around the limit

```python
while url:
    response = session.get(url)
    if response.status_code == 429:
        print('Rate Limited! Please wait')
        time.sleep(int(response.headers['retry-after']))
        continue
    if response.status_code != 200:
        print(f'Error with status code {response.status_code}')
        break

    data = response.json()
    df = df.append(data['results'])

    counter += 1
    url = data['next_page']
    time.sleep(1)
```