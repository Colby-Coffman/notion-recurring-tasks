import { Client } from "@notionhq/client"

const notion = new Client({ auth: "**************************" })

const databaseId = "****************************"

const myArgs = process.argv.slice(2);

async function addItem() {
  try {
    const response = await notion.pages.create({
      parent: { database_id: databaseId },
      properties: {
        title: { 
          title:[
            {
              "text": {
                "content": myArgs[0]
              }
            }
          ]
        },
        "Do Date": {
	  "date": {
          "start": myArgs[2],
          }
        },
        "Priority": {
          "select": {
            "name": myArgs[1],
            }
        },
      },
    })
    console.log(response)
    console.log("Success! Entry added.")
  } catch (error) {
    console.error(error.body)
  }
}

addItem()
