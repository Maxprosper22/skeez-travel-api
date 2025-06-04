console.log("OS", Deno.build.os)

const command = new Deno.Command("sanic", {
  args: ["src.main:create_app", "-p 8080", "-R src", "--dev"],
});
const process = command.spawn();
