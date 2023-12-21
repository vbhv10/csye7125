const { Client } = require('pg');
const { Kafka } = require('kafkajs');
const util = require('util');
const exec = util.promisify(require('child_process').exec);
require('dotenv').config()

const clientDb = new Client({
    user: process.env.DB_USER,
    host: process.env.DB_HOST,
    database: process.env.DB_NAME,
    password: process.env.DB_PASSWORD,
    port: process.env.DB_PORT,
});

async function getControllerHostnames(namespace) {
    const hostnameCommand = `curl -k -H "Authorization: Bearer $(cat /var/run/secrets/kubernetes.io/serviceaccount/token)" https://kubernetes.default.svc/api/v1/namespaces/${namespace}/pods 2>/dev/null | grep -o '\"hostname\": \"[^\"]*' | cut -d " " -f 2 | sed 's/\"//g' | grep 'controller'`;
    try {
        const { stdout, stderr } = await exec(hostnameCommand);
        if (stderr) {
            console.error(`Command execution error: ${stderr}`);
            return [];
        }
        return stdout.split("\n");
    } catch (error) {
        console.error(`Error: ${error.message}`);
        process.exit()
    }
}

async function commands() {
    try {
    const namespace = process.env.KAFKA_NAMESPACE
    let hostnames = []
    if (namespace) {
        hostnames = await getControllerHostnames(namespace);
        console.log(`Command output: ${hostnames}`);
    }
    const broker_list = hostnames.map((name) => {
        const prefix = name.split("controller")[0];
        return `${name}.${prefix}controller-headless.${namespace}.svc.cluster.local:9092`;
    });
    console.log(broker_list)
    return broker_list
} catch (error) {
    console.error(`Error: ${error.message}`);
    process.exit()
}
}

const run = async (broker_list) => {
    if(broker_list.length===0){
        broker_list = ['localhost']
    }
    const kafka = new Kafka({
        clientId: process.env.KAFKA_TOPIC+'-id',
        brokers: broker_list,
    });
    const consumer = kafka.consumer({ groupId: process.env.KAFKA_TOPIC+'-group' });

    await clientDb.connect();
    await consumer.connect();
    await consumer.subscribe({ topic: process.env.KAFKA_TOPIC, fromBeginning: false }); // Set fromBeginning to false

    await consumer.run({
        eachMessage: async ({ topic, partition, message }) => {
            let decodedMessage = Buffer.from(message.value, 'utf8').toString('utf8');
            decodedMessage = JSON.parse(decodedMessage)
            console.log(decodedMessage)

            const startTime = decodedMessage["start_time"]
            const endTime = decodedMessage["end_time"]
            const content = JSON.stringify(decodedMessage["content"]);
            const statusCode = decodedMessage["status_code"]
            const contentLength = decodedMessage["content_length"]
            const url = decodedMessage["url"]

            console.log("content : ", content)

            // Process each received message here
            // Insert data into PostgreSQL
            clientDb.query(
                `INSERT INTO ${process.env.DB_TABLE} (start_time, end_time, content, status_code, content_length, url) VALUES ($1, $2, $3, $4, $5, $6)`,
                [startTime, endTime, content, statusCode, contentLength, url],
                (err, result) => {
                  console.log("Here");
                  if (err) {
                    console.error('Error inserting data:', err);
                    process.exit();
                  } else {
                    console.log('Data inserted successfully');
                  }
                }
              );
        },
    });
};

commands()
    .then((broker_list)=>{
        run(broker_list)
            .catch((error) => {
            console.error('Error:', error);
        });
    })
    .catch((error) => {
    console.error('Error:', error);
})