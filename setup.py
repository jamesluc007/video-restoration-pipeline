import yaml
from dataclasses import dataclass, field
from typing import List

@dataclass
class DockerService:
    """
    Base class representing a Docker service.
    """
    image: str
    container_name: str
    environment: List[str] = field(default_factory=list)
    volumes: List[str] = field(default_factory=list)
    command: str = ""
    tty: bool = True
    stdin_open: bool = True
    restart: str = "no"
    deploy: dict = field(default_factory=lambda: {
        'resources': {
            'reservations': {
                'devices': [{
                    'driver': 'nvidia',
                    'count': 'all',
                    'capabilities': ['gpu']
                }]
            }
        }
    })

@dataclass
class RifeService(DockerService):
    """
    Class representing the Rife AI service.
    """
    pass

@dataclass
class DeoldifyService(DockerService):
    """
    Class representing the Deoldify service.
    """
    pass

@dataclass
class NeuralStyleService(DockerService):
    """
    Class representing the Neural Style Transfer service.
    """
    pass

@dataclass
class EsrganService(DockerService):
    """
    Class representing the ESRGAN service.
    """
    pass

def load_config(file_path: str):
    """
    Load configuration from a YAML file.

    :param file_path: Path to the YAML configuration file.
    :return: Parsed configuration dictionary.
    """
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def create_service(service_class, config, common_env, volumes):
    """
    Create a Docker service instance.

    :param service_class: The class of the Docker service.
    :param config: Dictionary containing service configuration.
    :param common_env: List of common environment variables.
    :param volumes: List of volumes to mount.
    :return: An instance of the Docker service.
    """
    service = service_class(
        image=config['image'],
        container_name=config['container_name'],
        environment=common_env + config.get('environment', []),
        volumes=volumes,
        command=config['command']
    )
    return service

def create_docker_compose(config):
    """
    Create the Docker Compose services based on the configuration.

    :param config: Configuration dictionary.
    :return: List of Docker service instances.
    """
    services = []

    common_env = []
    if config.get('NVIDIA_VISIBLE_DEVICES'):
        common_env.append(f"NVIDIA_VISIBLE_DEVICES={config['NVIDIA_VISIBLE_DEVICES']}")

    volumes = {
        'rife': ['./video/source:/video/source', './video/intermediate_1:/video/result'],
        'deoldify': ['./video/intermediate_1:/video/source', './video/intermediate_2:/video/result'],
        'neural_style': ['./video/intermediate_2:/video/source', './video/intermediate_3:/video/result'],
        'esrgan': ['./video/intermediate_3:/video/source', './video/result:/video/results']
    }

    # Adjust volumes based on which services are enabled
    if not config['rife']:
        volumes['deoldify'][0] = './video/source:/video/source'

    if not config['deoldify']:
        if not config['rife']:
            volumes['neural_style'][0] = './video/source:/video/source'
        else:
            volumes['neural_style'][0] = './video/intermediate_1:/video/source'

    if not config['neural_style']:
        if not config['deoldify'] and not config['rife']:
            volumes['esrgan'][0] = './video/source:/video/source'
        elif not config['deoldify']:
            volumes['esrgan'][0] = './video/intermediate_1:/video/source'
        else:
            volumes['esrgan'][0] = './video/intermediate_2:/video/source'

    # Create services in the specified order
    if config['rife']:
        rife_service = create_service(
            RifeService,
            {
                'image': 'rife-container',
                'container_name': 'rife_ai',
                'command': 'python inference_video.py --video /video/source/video.mp4 --output /video/result/video.mp4'
            },
            common_env,
            volumes['rife']
        )
        services.append(rife_service)

    if config['deoldify']:
        deoldify_service = create_service(
            DeoldifyService,
            {
                'image': 'deoldify',
                'container_name': 'deoldify',
                'command': f'python colorize_video.py --file_name video.mp4 --render_factor 30'
            },
            common_env,
            volumes['deoldify']
        )
        services.append(deoldify_service)

    if config['neural_style']:
        neural_style_service = create_service(
            NeuralStyleService,
            {
                'image': 'video-style-transfer',
                'container_name': 'neural_style',
                'command': f'python inference_video.py --file_name video.mp4 --model_name {config["NEURAL_MODEL"]}'
            },
            common_env,
            volumes['neural_style']
        )
        services.append(neural_style_service)

    if config['esrgan']:
        esrgan_service = create_service(
            EsrganService,
            {
                'image': 'esrgan',
                'container_name': 'esrgan',
                'command': f'python inference_realesrgan_video.py -i /video/source/video.mp4 -n RealESRGAN_x4plus --outscale {config["ESRGAN_OUTSCALE"]}'
            },
            common_env,
            volumes['esrgan']
        )
        services.append(esrgan_service)

    return services

def generate_docker_compose_yml(services, output_file='docker-compose.yml'):
    """
    Generate the Docker Compose YAML file.

    :param services: List of Docker service instances.
    :param output_file: Path to the output Docker Compose YAML file.
    """
    compose_dict = {
        'version': '3.8',
        'services': {}
    }
    for service in services:
        service_dict = {
            'image': service.image,
            'container_name': service.container_name,
            'environment': service.environment,
            'volumes': service.volumes,
            'command': service.command,
            'tty': service.tty,
            'stdin_open': service.stdin_open,
            'restart': service.restart,
            'deploy': service.deploy
        }
        compose_dict['services'][service.container_name] = service_dict

    with open(output_file, 'w') as file:
        yaml.dump(compose_dict, file)

if __name__ == "__main__":
    # Load configuration and create Docker Compose services
    config = load_config('config.yml')
    services = create_docker_compose(config)
    # Generate the Docker Compose YAML file
    generate_docker_compose_yml(services)
