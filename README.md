# City Analytics on the Cloud

A Cloud-based application that exploits a multitude of virtual machines (VMs) across the UniMelb Research Cloud (Nectar) for harvesting tweets through the Twitter APIs. The application also include a front-end interface for visualising our analysis and RESTFul API server for data accessing.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

*The VMs we use are provided by UniMelb Research Cloud (Nectar), which is based on OpenStack. And the Ansible playbook in `ansible/playbooks` mainly use OpenStack modules to create machines on the Instance Initialize Process. The following setting is based on UniMelb Research Cloud. You can change the code inside based on your cloud suppliers.*

#### Gain access to cloud providers

To gain access to UniMelb Research Cloud:

1. Login to https://dashboard.cloud.unimelb.edu.au. 
2. Download *openrc.sh* from Dashboard.
   * Make sure the correct project is selected
   * Download the OpenStack RC File
3. Reset API password
   * Dashboard -> User -> Settings -> Reset Password
4. Replace the `ansible/openrc.sh` with your own one. We suggest changing the `OS_PASSWORD` to your API password so that you don't have to input it every time.
5. Generate a ssh key pair in the cloud and put the private one to your `~/.ssh/`

#### Set the variable for the Ansible Playbook







```

```

### Installing

A step by step series of examples that tell you how to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc

