import bluetooth


PORT = 5  # ネット記事だとPORT=1と記述していることが多いですが、OSErrorが出ます！


def main():
    global PORT

    for addr, name in bluetooth.discover_devices(lookup_names=True):
        print(f'{addr} - {name}')

    server = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    server.bind(('', PORT))
    server.listen(1)

    uuid = "00001101-0000-1000-8000-00805F9B34FB"
    bluetooth.advertise_service(
        server,
        "SampleServer",
        service_id=uuid,
        service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
        profiles=[bluetooth.SERIAL_PORT_PROFILE]
    )

    sock, addr = server.accept()
    print(f'Accepted connection from {addr}')

    try:
        while True:
            data = sock.recv(1024)
            if not data:
                break
            print(f'Received: {data}')

    finally:
        sock.close()
        server.close()


if __name__ == '__main__':
    main()
