const sseService = new EventSourceService('http://localhost:8080/trips/sse');
sseService.connect();

console.log(sseService)
