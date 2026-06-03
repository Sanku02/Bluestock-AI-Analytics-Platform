function Loader() {

  return (

    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: "300px"
      }}
    >

      <div
        style={{
          width: "60px",
          height: "60px",
          border:
            "6px solid #e2e8f0",
          borderTop:
            "6px solid #2563eb",
          borderRadius: "50%",
          animation:
            "spin 1s linear infinite"
        }}
      />

    </div>

  );

}

export default Loader;