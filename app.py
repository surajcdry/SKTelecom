from bs4 import BeautifulSoup
import requests
import csv

def fetch_html(url):
    """Fetch the HTML content of the SK Telecom plans page"""
    # Error handling in case the request fails
    try:
        response = requests.get(url).text
        return response
    except requests.RequestException as e:
        print(f"An error occurred while fetching the HTML content: {e}")
        return None
    
def parse_html(html):
    """Parse the HTML content using BeautifulSoup and extract the plan names and benefits"""
    soup = BeautifulSoup(html, 'lxml')
    plan_table = soup.find("table", {"summary": "T PLAN Service Information. Plan, Monthly rate(including VAT), Talk/Text, Data, Benefits, T Plan & T family Benefits"})
    plan_table = plan_table.find("tbody") if plan_table else None
    plan_list = []

    if plan_table:
        rows = plan_table.find_all("tr")
        for row in rows: # skipping the header row
            # Extract the plan name and details
            name = row.find('th').text.strip()
            tds = row.find_all('td')
            
            price = tds[0].text.strip()
            try:
                benefits = tds[1].text.strip()
                data = tds[2].text.strip()
            except:
                benefits = "Same as previous plan"
                data = tds[1].text.strip()

            # Add the plan to the list
            if (name, price, benefits, data) not in plan_list:
                plan_list.append((name, price, benefits, data))

    return plan_list

def print_plans(plan_list):
    """Print plan details"""

    """Print plan details"""
    print(f"\nNumber of plans found: {len(plan_list)}")
    print("\nSK Telecom Cell Phone Plans\n")
    print("(Check latest prices at: https://www.tworld.co.kr/poc/eng/html/EN1.8T.html)\n")
    
    for i, plan in enumerate(plan_list, 1):
        name, price, benefits, data = plan
        
        # Handle encoding issues by replacing problematic characters with ￦
        price = price.replace('ï¿¦', '￦')
        benefits = benefits.encode('ascii', 'replace').decode()
        data = data.encode('ascii', 'replace').decode()
        data = data.replace('???', "'")
        data = data.replace('\n', "")
        data = data.replace('\t', "")
        
        print(f"{i}. {name}")
        print(f"\tPrice: {price}")
        print(f"\tBenefits: {benefits}")
        print(f"\tData: {data}\n")

def save_to_csv(plan_list):
    """Save the plans to a CSV file"""
    csv_file = 'plans.csv'
    
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write header
        writer.writerow(['Name', 'Price', 'Benefits', 'Data'])
        
        # Write plan data
        for plan in plan_list:
            name, price, benefits, data = plan
            # Clean up the data before writing
            price = price.replace('ï¿¦', '￦')
            benefits = benefits.encode('ascii', 'replace').decode()
            data = data.encode('ascii', 'replace').decode()
            data = data.replace('???', "'")
            data = data.replace('\n', "")
            data = data.replace('\t', "")
            writer.writerow([name, price, benefits, data])
    
    print(f"\nPlans have been saved to {csv_file}")

def main():
    url = 'https://www.tworld.co.kr/poc/eng/html/EN1.8T.html'
    html = fetch_html(url)
    if html:
        plan_list = parse_html(html)
        print_plans(plan_list)
        save_to_csv(plan_list)

if __name__ == '__main__':
    main()